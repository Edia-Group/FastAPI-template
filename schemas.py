from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional
from datetime import datetime

class UserUpdate(BaseModel):
    username: str
    full_name: str
    date_of_birth: date
    gender: str

class UserCreate(BaseModel):
    phone_number: str
    full_name: str
    email: str

class VerifyToken(BaseModel):
    phone_number: str
    otp: str

class PhoneRequest(BaseModel):
    phone_number: str

class PostCreate(BaseModel):
    title: str
    description: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    user_phone_number: str
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

