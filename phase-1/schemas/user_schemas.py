from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    subscription_tier: str
    created_at: datetime

    class Config:
        from_attributes = True
