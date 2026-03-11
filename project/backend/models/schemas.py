from pydantic import BaseModel, Field


class RegisterUser(BaseModel):
    telegram_id: int
    username: str | None = None
    phone_number: str
    ip: str | None = None
    referrer_id: int | None = None


class DepositCreate(BaseModel):
    user_id: int
    currency: str
    amount: float = Field(gt=0)
    tx_hash: str | None = None
    screenshot_url: str | None = None


class WithdrawalCreate(BaseModel):
    user_id: int
    currency: str
    amount: float = Field(gt=0)
    address: str
    telegram_code: str = Field(min_length=4, max_length=8)


class SwapRequest(BaseModel):
    user_id: int
    from_currency: str
    to_currency: str
    amount: float = Field(gt=0)


class TransferRequest(BaseModel):
    from_user_id: int
    to_user_identifier: str
    currency: str
    amount: float


class PromoCreate(BaseModel):
    code: str
    reward_type: str
    reward_value: float
