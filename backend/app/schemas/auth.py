from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: str
    username: str
    role: str
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str
    user: UserInfo


class UserProfile(BaseModel):
    id: str
    username: str
    role: str
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
