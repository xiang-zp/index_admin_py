from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from app.database import Base


class Review(Base):
    """用户评价表"""
    __tablename__ = "reviews"
    
    id = Column(String(32), primary_key=True, comment="评价唯一标识ID")
    name = Column(String(50), nullable=False, comment="评价者姓名")
    avatar_color = Column(String(20), nullable=False, default="indigo", comment="头像颜色，如indigo、blue等")
    rating = Column(Integer, nullable=False, index=True, comment="评分，1-5星")
    content = Column(Text, nullable=False, comment="评价内容")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
