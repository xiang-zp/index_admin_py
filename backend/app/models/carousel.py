from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class Carousel(Base):
    """轮播文案表"""
    __tablename__ = "carousels"
    
    id = Column(String(32), primary_key=True, comment="轮播文案唯一标识ID")
    title = Column(String(100), nullable=False, comment="轮播标题")
    description = Column(Text, nullable=True, comment="轮播描述信息")
    is_visible = Column(Boolean, default=True, nullable=False, index=True, comment="是否在前端显示")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序，数字越小越靠前")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
