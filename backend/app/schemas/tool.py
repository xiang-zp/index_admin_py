from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ToolBase(BaseModel):
    name: str
    description: str
    path: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    row: Optional[str] = 'row1'
    is_visible: bool = True
    is_active: bool = True


class ToolCreate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    row: Optional[str] = 'row1'
    is_visible: bool = True


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    row: Optional[str] = None
    is_visible: Optional[bool] = None
    is_active: Optional[bool] = None


class ToolResponse(BaseModel):
    id: str
    name: str
    description: str
    path: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    row: Optional[str] = 'row1'
    is_visible: bool
    is_active: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ToolToggleRequest(BaseModel):
    is_visible: bool
