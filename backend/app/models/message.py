from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(String(255), primary_key=True, comment="消息唯一标识ID")
    conversation_id = Column(String(255), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属会话ID")
    content = Column(Text, nullable=False, comment="消息内容")
    is_user = Column(Boolean, nullable=False, comment="是否为用户消息，true为用户，false为AI")
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True, comment="消息时间戳")
