from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(50), unique=True)
    ip: Mapped[str | None] = mapped_column(String(50), nullable=True)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.user)
    referrer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    vip_level: Mapped[int] = mapped_column(Integer, default=0)
    turnover: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    balances: Mapped[list["Balance"]] = relationship(back_populates="user")


class Balance(Base):
    __tablename__ = "balances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    currency: Mapped[str] = mapped_column(String(20), index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 8), default=0)
    frozen_balance: Mapped[float] = mapped_column(Numeric(18, 8), default=0)

    user: Mapped[User] = relationship(back_populates="balances")


class DepositRequest(Base):
    __tablename__ = "deposit_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    currency: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Numeric(18, 8))
    tx_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    screenshot_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[RequestStatus] = mapped_column(SqlEnum(RequestStatus), default=RequestStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WithdrawalRequest(Base):
    __tablename__ = "withdrawal_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    currency: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Numeric(18, 8))
    address: Mapped[str] = mapped_column(String(255))
    telegram_code: Mapped[str] = mapped_column(String(8))
    status: Mapped[RequestStatus] = mapped_column(SqlEnum(RequestStatus), default=RequestStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ExchangeOperation(Base):
    __tablename__ = "exchange_operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    from_currency: Mapped[str] = mapped_column(String(20))
    to_currency: Mapped[str] = mapped_column(String(20))
    from_amount: Mapped[float] = mapped_column(Numeric(18, 8))
    to_amount: Mapped[float] = mapped_column(Numeric(18, 8))
    rate: Mapped[float] = mapped_column(Float)
    fee_amount: Mapped[float] = mapped_column(Numeric(18, 8), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    reward_type: Mapped[str] = mapped_column(String(20))
    reward_value: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class CheckCode(Base):
    __tablename__ = "check_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    currency: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Numeric(18, 8))
    is_redeemed: Mapped[bool] = mapped_column(Boolean, default=False)
    redeemed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(120), unique=True)
    value: Mapped[str] = mapped_column(Text)


class TransactionHash(Base):
    __tablename__ = "transaction_hashes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tx_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[str] = mapped_column(String(255))
    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
