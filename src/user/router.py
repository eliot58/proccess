from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from src.core.settings import API_KEY, DEPOSIT_ADDRESSES
from src.user.models import User
from src.user.schemas import CreateUserSchemas, DepositSchemas, WithdrawSchemas
from tortoise.exceptions import IntegrityError

router = APIRouter(tags=["user"])

api_key_header = APIKeyHeader(name="X-API-Key")

@router.post("/user/")
async def create_user(user: CreateUserSchemas, api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API-Key")
    
    try:
        user = await User.create(**user.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with this tg_id already exists")
    
    return user

@router.get("/user/{tg_id}/")
async def get_user(tg_id: str):
    user = await User.get_or_none(tg_id=tg_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/deposit/{tg_id}/")
async def deposit(tg_id: str, data: DepositSchemas):
    user = await User.get_or_none(tg_id=tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return f"ton://transfer/{DEPOSIT_ADDRESSES[data.currency.value]}?amount={data.amount * 1000000000}&text={user.id}"

@router.post("/withdraw/{tg_id}/")
async def withdraw(tg_id: str, data: WithdrawSchemas, api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API-Key")
    
    return None