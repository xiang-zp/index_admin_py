from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Activity(Base):
    """活动记录表"""
    __tablename__ = "activities"
    
    id = Column(String(32), primary_key=True, comment="活动记录唯一标识ID")
    type = Column(String(50), nullable=False, index=True, comment="活动类型：agent、tool、document、review、user、role_change等")
    message = Column(Text, nullable=False, comment="活动描述消息")
    user_id = Column(String(32), nullable=True, index=True, comment="执行操作的管理员ID")
    target_id = Column(String(32), nullable=True, index=True, comment="目标对象ID")
    target_type = Column(String(50), nullable=True, comment="目标对象类型")
    details = Column(JSON, nullable=True, comment="额外详情，JSON格式")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="创建时间")