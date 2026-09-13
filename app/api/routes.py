import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.domain import User, APIKey, UsageRecord, Invoice
from app.schemas.domain import (
    UserCreate, UserResponse,
    APIKeyCreate, APIKeyResponse,
    UsageRecordCreate, UsageRecordResponse,
    InvoiceResponse
)

# Initialize router before using decorator routes
router = APIRouter()

# Model Pricing (Per 1,000 Tokens)
MODEL_PRICING = {
    "gpt-4o": {"input": 0.0025, "output": 0.010},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015}
}

# 1. User Endpoints
@router.post("/users", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(email=user_in.email, name=user_in.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 2. API Key Endpoints
@router.post("/keys", response_model=APIKeyResponse)
def generate_api_key(key_in: APIKeyCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == key_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    generated_key = f"sk_live_{secrets.token_hex(16)}"
    api_key = APIKey(key=generated_key, user_id=user.id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

# 3. Usage Metering Endpoint
@router.post("/usage", response_model=UsageRecordResponse)
def log_usage(usage_in: UsageRecordCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == usage_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    pricing = MODEL_PRICING.get(usage_in.model_name, {"input": 0.001, "output": 0.002})
    
    prompt_cost = (usage_in.prompt_tokens / 1000.0) * pricing["input"]
    completion_cost = (usage_in.completion_tokens / 1000.0) * pricing["output"]
    total_cost = round(prompt_cost + completion_cost, 6)
    total_tokens = usage_in.prompt_tokens + usage_in.completion_tokens
    
    record = UsageRecord(
        user_id=user.id,
        model_name=usage_in.model_name,
        prompt_tokens=usage_in.prompt_tokens,
        completion_tokens=usage_in.completion_tokens,
        total_tokens=total_tokens,
        cost=total_cost
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# 4. Generate Monthly Invoice Endpoint
@router.post("/invoices/generate/{user_id}", response_model=InvoiceResponse)
def generate_invoice(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    usage_records = db.query(UsageRecord).filter(UsageRecord.user_id == user_id).all()
    total_amount = sum(record.cost for record in usage_records)

    if total_amount <= 0:
        raise HTTPException(status_code=400, detail="No usage records found to bill")

    invoice = Invoice(
        user_id=user.id,
        amount_due=round(total_amount, 6),
        status="pending"
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice