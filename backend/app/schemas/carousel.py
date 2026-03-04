from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CarouselBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_visible: bool = True


class CarouselCreate(CarouselBase):
    pass


class CarouselUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_visible: Optional[bool] = None


class CarouselResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    is_visible: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CarouselReorderRequest(BaseModel):
    ids: List[str]


class CarouselToggleRequest(BaseModel):
    is_visible: bool
