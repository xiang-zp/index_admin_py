from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    category: str
    title: str
    description: str
    color: str = "#3b82f6"
    url: Optional[str] = None
    row: str = "row1"
    is_visible: bool = True


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    url: Optional[str] = None
    row: Optional[str] = None
    is_visible: Optional[bool] = None


class DocumentResponse(BaseModel):
    id: str
    category: str
    title: str
    description: str
    color: str
    url: Optional[str] = None
    row: str
    is_visible: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    items: List[DocumentResponse]
    total: int


class CategoryResponse(BaseModel):
    id: str
    name: str
    color: str


class CategoryCreate(BaseModel):
    name: str
    color: str = "#3b82f6"


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponseFull(BaseModel):
    id: int
    name: str
    color: str
    is_active: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
