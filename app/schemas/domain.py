from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Key Schemas ---
class APIKeyCreate(BaseModel):
    user_id: str

class APIKeyResponse(BaseModel):
    id: str
    key: str
    user_id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Usage Log Schemas ---
class UsageRecordCreate(BaseModel):
    user_id: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int

class UsageRecordResponse(BaseModel):
    id: str
    user_id: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Invoice Schemas ---
class InvoiceResponse(BaseModel):
    id: str
    user_id: str
    amount_due: float
    status: str
    stripe_payment_intent_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True