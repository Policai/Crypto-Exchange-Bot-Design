from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.entities import Balance, User
from backend.models.schemas import RegisterUser

router = APIRouter(prefix="/users", tags=["users"])
DEFAULT_CURRENCIES = ["USDT_TRON", "USDT_TON", "TON", "TRX", "BTC", "LTC", "RUB"]


@router.post("/register")
def register_user(payload: RegisterUser, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.telegram_id == payload.telegram_id).first()
    if existing:
        return {"id": existing.id, "message": "already_registered"}

    user = User(**payload.model_dump())
    db.add(user)
    db.flush()

    for currency in DEFAULT_CURRENCIES:
        db.add(Balance(user_id=user.id, currency=currency, amount=0, frozen_balance=0))

    db.commit()
    return {"id": user.id, "message": "registered"}


@router.get("/{user_id}/balances")
def get_balances(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    return [{"currency": b.currency, "amount": float(b.amount), "frozen": float(b.frozen_balance)} for b in user.balances]
