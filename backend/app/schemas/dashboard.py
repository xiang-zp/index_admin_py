from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class DashboardStats(BaseModel):
    agents: int
    tools: int
    documents: int
    reviews: int
    users: int


class ActivityBase(BaseModel):
    type: str
    message: str
    user_id: Optional[str] = None
    target_id: Optional[str] = None
    target_type: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(BaseModel):
    id: int
    type: str
    message: str
    time: datetime
    user_id: Optional[str] = None
    target_id: Optional[str] = None
    target_type: Optional[str] = None
    
    class Config:
        from_attributes = True
