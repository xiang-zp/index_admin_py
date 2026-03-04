from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuthCodeBase(BaseModel):
    description: Optional[str] = None
    invite_code: str
    auth_location: str = "global"


class AuthCodeCreate(AuthCodeBase):
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class AuthCodeUpdate(BaseModel):
    description: Optional[str] = None
    auth_location: Optional[str] = None
    status: Optional[str] = None
    expire_time: Optional[str] = None


class AuthCodeResponse(BaseModel):
    id: str
    description: Optional[str] = None
    invite_code: str
    status: str
    auth_location: str
    authorized_user: Optional[str] = None
    authorized_at: Optional[datetime] = None
    expire_time: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
