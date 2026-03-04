from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Date
from sqlalchemy.sql import func
from app.database import Base


class Project(Base):
    """项目表"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="项目ID，自增主键")
    category = Column(String(255), nullable=False, index=True, comment="项目分类")
    title = Column(String(500), nullable=False, comment="项目标题")
    description = Column(Text, nullable=False, comment="项目描述信息")
    date = Column(Date, nullable=False, index=True, comment="项目日期")
    color = Column(String(255), nullable=False, comment="项目显示颜色")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
