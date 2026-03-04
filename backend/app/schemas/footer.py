from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FooterConfigBase(BaseModel):
    logo_url: Optional[str] = None
    slogan: Optional[str] = None


class FooterConfigUpdate(FooterConfigBase):
    pass


class FooterConfigResponse(BaseModel):
    logo_url: Optional[str] = None
    slogan: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class FooterLinkBase(BaseModel):
    title: str
    url: str


class FooterLinkCreate(FooterLinkBase):
    pass


class FooterLinkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None


class FooterLinkResponse(BaseModel):
    id: str
    title: str
    url: str
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
