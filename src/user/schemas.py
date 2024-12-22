from pydantic import BaseModel
from .enum import Currency


class CreateUserSchemas(BaseModel):
    tg_id: str
    

class WithdrawSchemas(BaseModel):
    address: str
    currency: Currency
    amount: float


class DepositSchemas(BaseModel):
    currency: Currency
    amount: float