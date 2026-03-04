from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentToggleRequest
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_agents(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        agents = db.query(Agent).order_by(Agent.sort_order).all()
        return APIResponse.success(data=[
            {
                "id": agent.id,
                "name": agent.name,
                "api": agent.api,
                "source": agent.source,
                "bot_id": agent.bot_id,
                "is_visible": agent.is_visible,
                "sort_order": agent.sort_order,
                "created_at": agent.created_at.isoformat() if agent.created_at else None,
                "updated_at": agent.updated_at.isoformat() if agent.updated_at else None
            }
            for agent in agents
        ])
    except Exception as e:
        logger.error(f"Get agents error: {e}")
        return APIResponse.error(f"获取智能体列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_agent(
    request: AgentCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        max_order = db.query(Agent).count()
        agent = Agent(
            id=f"AGENT-{uuid.uuid4().hex[:8].upper()}",
            name=request.name,
            api=request.api,
            source=request.source,
            bot_id=request.bot_id,
            is_visible=request.is_visible,
            sort_order=max_order
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        
        # 记录创建智能体活动
        create_simple_activity(
            db=db,
            activity_type="agent_create",
            message=f"创建智能体 '{agent.name}'",
            user_id=current_user.id,
            target_id=agent.id,
            target_type="agent",
            details={
                "name": agent.name,
                "api": agent.api,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Agent created: {agent.id}")
        return APIResponse.success(data={
            "id": agent.id,
            "name": agent.name,
            "api": agent.api,
            "source": agent.source,
            "bot_id": agent.bot_id,
            "is_visible": agent.is_visible,
            "sort_order": agent.sort_order,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "updated_at": agent.updated_at.isoformat() if agent.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create agent error: {e}")
        db.rollback()
        return APIResponse.error(f"创建智能体失败: {str(e)}", 500)


@router.put("/{agent_id}", response_model=dict)
async def update_agent(
    agent_id: str,
    request: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return APIResponse.error("智能体不存在", 404)
        
        if request.name is not None:
            agent.name = request.name
        if request.api is not None:
            agent.api = request.api
        if request.source is not None:
            agent.source = request.source
        if request.bot_id is not None:
            agent.bot_id = request.bot_id
        if request.is_visible is not None:
            agent.is_visible = request.is_visible
        
        db.commit()
        db.refresh(agent)
        
        # 记录更新智能体活动
        create_simple_activity(
            db=db,
            activity_type="agent_update",
            message=f"更新智能体 '{agent.name}'",
            user_id=current_user.id,
            target_id=agent.id,
            target_type="agent",
            details={
                "name": agent.name,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Agent updated: {agent_id}")
        return APIResponse.success(data={
            "id": agent.id,
            "name": agent.name,
            "api": agent.api,
            "source": agent.source,
            "bot_id": agent.bot_id,
            "is_visible": agent.is_visible,
            "sort_order": agent.sort_order,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "updated_at": agent.updated_at.isoformat() if agent.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update agent error: {e}")
        db.rollback()
        return APIResponse.error(f"更新智能体失败: {str(e)}", 500)


@router.delete("/{agent_id}", response_model=dict)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return APIResponse.error("智能体不存在", 404)
        
        # 记录删除智能体活动
        create_simple_activity(
            db=db,
            activity_type="agent_delete",
            message=f"删除智能体 '{agent.name}'",
            user_id=current_user.id,
            target_id=agent.id,
            target_type="agent",
            details={
                "name": agent.name,
                "operator_username": current_user.username
            }
        )
        
        db.delete(agent)
        db.commit()
        
        logger.info(f"Agent deleted: {agent_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete agent error: {e}")
        db.rollback()
        return APIResponse.error(f"删除智能体失败: {str(e)}", 500)


@router.patch("/{agent_id}/toggle", response_model=dict)
async def toggle_agent(
    agent_id: str,
    request: AgentToggleRequest,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return APIResponse.error("智能体不存在", 404)
        
        agent.is_visible = request.is_visible
        db.commit()
        
        # 记录切换智能体可见性活动
        create_simple_activity(
            db=db,
            activity_type="agent_toggle",
            message=f"设置智能体 '{agent.name}' 为 {'显示' if request.is_visible else '隐藏'}",
            user_id=current_user.id,
            target_id=agent.id,
            target_type="agent",
            details={
                "name": agent.name,
                "is_visible": request.is_visible,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Agent toggled: {agent_id} -> {request.is_visible}")
        return APIResponse.success(message="状态更新成功")
    except Exception as e:
        logger.error(f"Toggle agent error: {e}")
        db.rollback()
        return APIResponse.error(f"切换状态失败: {str(e)}", 500)
