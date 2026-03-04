from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Conversation(Base):
    """对话表"""
    __tablename__ = "conversations"
    
    id = Column(String(255), primary_key=True, comment="对话唯一标识ID")
    user_id = Column(String(255), nullable=False, index=True, comment="用户ID")
    agent_id = Column(String(255), nullable=False, index=True, comment="智能体ID")
    title = Column(String(500), nullable=True, comment="对话标题")
    is_terminated = Column(Boolean, default=False, nullable=False, comment="是否已终止")
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
