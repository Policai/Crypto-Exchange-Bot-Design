from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.entities import Balance, DepositRequest, ExchangeOperation, RequestStatus, TransactionHash, User, WithdrawalRequest
from backend.models.schemas import DepositCreate, SwapRequest, TransferRequest, WithdrawalCreate
from backend.services.rates import get_rate
from backend.services.security import unique_comment

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post("/deposit")
def create_deposit(payload: DepositCreate, db: Session = Depends(get_db)):
    comment = unique_comment()
    while db.query(DepositRequest).filter(DepositRequest.comment == comment).first():
        comment = unique_comment()
    request = DepositRequest(**payload.model_dump(), comment=comment)
    db.add(request)
    db.commit()
    return {"status": "pending", "request_id": request.id, "memo": comment}


@router.post("/withdraw")
def create_withdraw(payload: WithdrawalCreate, db: Session = Depends(get_db)):
    bal = db.query(Balance).filter(Balance.user_id == payload.user_id, Balance.currency == payload.currency).first()
    if not bal or float(bal.amount) < payload.amount:
        raise HTTPException(status_code=400, detail="insufficient_funds")

    bal.amount = float(bal.amount) - payload.amount
    bal.frozen_balance = float(bal.frozen_balance) + payload.amount
    req = WithdrawalRequest(**payload.model_dump())
    db.add(req)
    db.commit()
    return {"status": "pending", "request_id": req.id}


@router.post("/transfer")
def internal_transfer(payload: TransferRequest, db: Session = Depends(get_db)):
    src = db.query(Balance).filter(Balance.user_id == payload.from_user_id, Balance.currency == payload.currency).first()
    if payload.to_user_identifier.isdigit():
        dst_user = db.query(User).filter(User.id == int(payload.to_user_identifier)).first()
    else:
        dst_user = db.query(User).filter(User.username == payload.to_user_identifier.replace("@", "")).first()
    if not src or not dst_user:
        raise HTTPException(status_code=404, detail="account_not_found")
    if float(src.amount) < payload.amount:
        raise HTTPException(status_code=400, detail="insufficient_funds")
    dst = db.query(Balance).filter(Balance.user_id == dst_user.id, Balance.currency == payload.currency).first()
    fee = payload.amount * 0.005
    src.amount = float(src.amount) - payload.amount
    dst.amount = float(dst.amount) + (payload.amount - fee)
    db.commit()
    return {"status": "success", "fee": fee}


@router.post("/swap")
async def instant_swap(payload: SwapRequest, db: Session = Depends(get_db)):
    src = db.query(Balance).filter(Balance.user_id == payload.user_id, Balance.currency == payload.from_currency).first()
    dst = db.query(Balance).filter(Balance.user_id == payload.user_id, Balance.currency == payload.to_currency).first()
    if not src or not dst:
        raise HTTPException(status_code=404, detail="balance_not_found")
    if float(src.amount) < payload.amount:
        raise HTTPException(status_code=400, detail="insufficient_funds")

    rate = await get_rate(payload.from_currency.replace("USDT_TRON", "USDT").replace("USDT_TON", "USDT"), payload.to_currency.replace("USDT_TRON", "USDT").replace("USDT_TON", "USDT"))
    result_amount = payload.amount * rate
    src.amount = float(src.amount) - payload.amount
    dst.amount = float(dst.amount) + result_amount

    op = ExchangeOperation(
        user_id=payload.user_id,
        from_currency=payload.from_currency,
        to_currency=payload.to_currency,
        from_amount=payload.amount,
        to_amount=result_amount,
        rate=rate,
        fee_amount=result_amount * 0.01,
    )
    db.add(op)
    db.commit()
    return {"status": "completed", "rate": rate, "received": result_amount}


@router.post("/cryptobot/webhook")
def cryptobot_webhook(payload: dict, db: Session = Depends(get_db)):
    tx_hash = payload.get("tx_hash")
    user_id = payload.get("user_id")
    currency = payload.get("currency", "USDT_TRON")
    amount = float(payload.get("amount", 0))
    if not tx_hash or not user_id or amount <= 0:
        raise HTTPException(status_code=400, detail="invalid_payload")
    if db.query(TransactionHash).filter(TransactionHash.tx_hash == tx_hash).first():
        raise HTTPException(status_code=409, detail="duplicate_transaction")

    db.add(TransactionHash(tx_hash=tx_hash))
    bal = db.query(Balance).filter(Balance.user_id == user_id, Balance.currency == currency).first()
    if not bal:
        raise HTTPException(status_code=404, detail="balance_not_found")
    bal.amount = float(bal.amount) + amount
    db.commit()
    return {"status": "credited"}


@router.post("/admin/approve-deposit/{request_id}")
def approve_deposit(request_id: int, db: Session = Depends(get_db)):
    req = db.query(DepositRequest).filter(DepositRequest.id == request_id).first()
    if not req or req.status != RequestStatus.pending:
        raise HTTPException(status_code=404, detail="request_not_found")
    bal = db.query(Balance).filter(Balance.user_id == req.user_id, Balance.currency == req.currency).first()
    bal.amount = float(bal.amount) + float(req.amount)
    req.status = RequestStatus.approved
    db.commit()
    return {"status": "approved"}
