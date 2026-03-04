from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    api: str
    source: str = "内置"
    bot_id: Optional[str] = None
    is_visible: bool = True
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api: Optional[str] = None
    source: Optional[str] = None
    bot_id: Optional[str] = None
    is_visible: Optional[bool] = None
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    api: str
    source: str
    bot_id: Optional[str] = None
    is_visible: bool
    is_active: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AgentToggleRequest(BaseModel):
    is_visible: bool
