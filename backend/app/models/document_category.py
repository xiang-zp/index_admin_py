from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class DocumentCategory(Base):
    """文档分类标签表"""
    __tablename__ = "document_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name = Column(String(50), nullable=False, unique=True, comment="分类名称")
    color = Column(String(20), nullable=False, default="#3b82f6", comment="分类显示颜色")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序顺序")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
