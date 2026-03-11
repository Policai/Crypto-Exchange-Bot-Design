from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.entities import DepositRequest, PromoCode, SystemSetting, User
from backend.models.schemas import PromoCreate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/promo")
def create_promo(payload: PromoCreate, db: Session = Depends(get_db)):
    promo = PromoCode(**payload.model_dump())
    db.add(promo)
    db.commit()
    return {"id": promo.id, "code": promo.code}


@router.patch("/users/{user_id}/block")
def block_user(user_id: int, blocked: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    user.is_blocked = blocked
    db.commit()
    return {"status": "updated", "blocked": blocked}


@router.post("/settings")
def set_setting(key: str, value: str, db: Session = Depends(get_db)):
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if setting:
        setting.value = value
    else:
        db.add(SystemSetting(key=key, value=value))
    db.commit()
    return {"status": "saved"}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    users = db.query(func.count(User.id)).scalar() or 0
    pending_deposits = db.query(func.count(DepositRequest.id)).scalar() or 0
    return {
        "users": users,
        "pending_operations": pending_deposits,
    }
