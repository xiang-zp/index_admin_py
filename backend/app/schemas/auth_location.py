from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuthLocationBase(BaseModel):
    value: str
    label: str
    description: Optional[str] = None


class AuthLocationCreate(AuthLocationBase):
    pass


class AuthLocationUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None


class AuthLocationResponse(BaseModel):
    id: str
    value: str
    label: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
