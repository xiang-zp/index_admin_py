import uuid
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.dashboard import ActivityCreate


def generate_activity_id() -> str:
    """生成活动记录ID"""
    return f"ACT-{uuid.uuid4().hex[:8].upper()}"


def create_activity(
    db: Session,
    activity_data: ActivityCreate,
    user_id: Optional[str] = None,
    target_id: Optional[str] = None,
    target_type: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Activity:
    """创建活动记录
    
    Args:
        db: 数据库会话
        activity_data: 活动数据
        user_id: 执行操作的管理员ID
        target_id: 目标对象ID
        target_type: 目标对象类型
        details: 额外详情
    
    Returns:
        Activity: 创建的活动记录
    """
    activity = Activity(
        id=generate_activity_id(),
        type=activity_data.type,
        message=activity_data.message,
        user_id=user_id,
        target_id=target_id,
        target_type=target_type,
        details=details or {}
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def create_simple_activity(
    db: Session,
    activity_type: str,
    message: str,
    user_id: Optional[str] = None,
    target_id: Optional[str] = None,
    target_type: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Activity:
    """简化版创建活动记录
    
    Args:
        db: 数据库会话
        activity_type: 活动类型
        message: 活动消息
        user_id: 执行操作的管理员ID
        target_id: 目标对象ID
        target_type: 目标对象类型
        details: 额外详情
    
    Returns:
        Activity: 创建的活动记录
    """
    activity_data = ActivityCreate(
        type=activity_type,
        message=message,
        user_id=user_id,
        target_id=target_id,
        target_type=target_type,
        details=details
    )
    return create_activity(db, activity_data, user_id, target_id, target_type, details)


def record_role_change_activity(
    db: Session,
    user_id: str,
    target_user_id: str,
    old_role: str,
    new_role: str,
    target_username: str,
    operator_username: Optional[str] = None
) -> Activity:
    """记录角色变更活动
    
    Args:
        db: 数据库会话
        user_id: 执行操作的管理员ID
        target_user_id: 目标用户ID
        old_role: 原角色
        new_role: 新角色
        target_username: 目标用户名
        operator_username: 操作者用户名
    
    Returns:
        Activity: 创建的活动记录
    """
    message = f"修改用户 '{target_username}' 的角色"
    if operator_username:
        message = f"{operator_username} {message}"
    
    details = {
        "old_role": old_role,
        "new_role": new_role,
        "target_user_id": target_user_id,
        "target_username": target_username,
        "operator_username": operator_username
    }
    
    return create_simple_activity(
        db=db,
        activity_type="role_change",
        message=message,
        user_id=user_id,
        target_id=target_user_id,
        target_type="user",
        details=details
    )