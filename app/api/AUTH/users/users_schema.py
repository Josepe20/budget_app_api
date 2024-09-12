from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    is_active: bool
    is_verified: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        from_attributes = True


