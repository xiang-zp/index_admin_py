from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.agent import Agent
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatRequest, TerminateRequest, TerminateResponse, Agent as AgentSchema
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from typing import Optional
import json
import uuid
import time

router = APIRouter()
logger = get_logger(__name__)


@router.get("/agents", response_model=dict)
async def get_agents(db: Session = Depends(get_db)):
    """
    获取智能体列表
    """
    try:
        agents = db.query(Agent).filter(Agent.is_active == True).all()
        
        agent_list = [
            AgentSchema(
                id=agent.id,
                name=agent.name,
                description=agent.description
            )
            for agent in agents
        ]
        
        return APIResponse.success(data=agent_list)
        
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return APIResponse.error(f"获取智能体列表失败: {str(e)}", 500)


@router.post("/terminate", response_model=dict)
async def terminate_task(
    request: TerminateRequest,
    db: Session = Depends(get_db)
):
    """
    终止任务
    """
    try:
        conv = db.query(Conversation).filter(
            Conversation.id == request.conversation_id
        ).first()
        
        if not conv:
            return APIResponse.error("对话不存在", 404)
        
        conv.is_terminated = True
        db.commit()
        
        logger.info(f"Conversation terminated: {request.conversation_id}")
        
        return APIResponse.success(
            data=TerminateResponse(
                conversation_id=request.conversation_id,
                terminated=True
            ),
            message="任务已终止"
        )
        
    except Exception as e:
        logger.error(f"Error terminating task: {e}")
        db.rollback()
        return APIResponse.error(f"终止任务失败: {str(e)}", 500)


@router.post("/send")
async def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """
    发送消息（SSE流式响应）
    """
    try:
        # 生成对话ID（如果不存在）
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # 创建对话（如果不存在）
        if not request.conversation_id:
            conv = Conversation(
                id=conversation_id,
                user_id="default_user",  # TODO: 从token获取真实用户ID
                agent_id=request.agent_id,
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message
            )
            db.add(conv)
        
        # 保存用户消息
        user_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=request.message,
            is_user=True
        )
        db.add(user_message)
        db.commit()
        
        # 模拟AI回复（流式）
        async def generate_response():
            response_text = f"这是一个模拟的AI回复。您的问题是：{request.message}。"
            
            # 模拟逐字输出
            for char in response_text:
                yield f"data: {json.dumps({'type': 'message', 'content': char}, ensure_ascii=False)}\n\n"
                time.sleep(0.05)  # 模拟打字速度
            
            # 保存AI消息到数据库
            ai_message = Message(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                content=response_text,
                is_user=False
            )
            db.add(ai_message)
            db.commit()
            
            # 发送完成信号
            yield f"data: {json.dumps({'type': 'done', 'content': ''})}\n\n"
        
        logger.info(f"Message sent to conversation: {conversation_id}")
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        db.rollback()
        async def error_response():
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        return StreamingResponse(error_response(), media_type="text/event-stream")
