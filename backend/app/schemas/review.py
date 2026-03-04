from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ReviewBase(BaseModel):
    name: str
    avatar_color: str = "indigo"
    rating: int
    content: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    name: Optional[str] = None
    avatar_color: Optional[str] = None
    rating: Optional[int] = None
    content: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    name: str
    avatar: Optional[str] = None
    avatar_color: str
    rating: int
    date: Optional[str] = None
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    list: List[ReviewResponse]
    total: int
