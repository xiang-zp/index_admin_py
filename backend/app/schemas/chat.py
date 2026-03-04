from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., description="用户消息")
    agent_id: str = Field(..., description="智能体ID")
    conversation_id: Optional[str] = Field(None, description="对话ID")


class TerminateRequest(BaseModel):
    """终止任务请求"""
    conversation_id: str = Field(..., description="对话ID")


class TerminateResponse(BaseModel):
    """终止任务响应"""
    conversation_id: str
    terminated: bool


class Agent(BaseModel):
    """智能体"""
    id: str
    name: str
    description: Optional[str] = None


class Message(BaseModel):
    """消息"""
    id: str
    content: str
    is_user: bool
    timestamp: datetime
