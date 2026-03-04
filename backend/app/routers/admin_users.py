from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.user import AdminUser
from app.schemas.user import UserCreate, UserUpdate
from app.utils.auth import get_password_hash
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import record_role_change_activity, create_simple_activity
from app.dependencies import get_current_user

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_users(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        users = db.query(AdminUser).order_by(AdminUser.created_at.desc()).all()
        return APIResponse.success(data=[
            {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
            for user in users
        ])
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return APIResponse.error(f"获取用户列表失败: {str(e)}", 500)


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
        if not user:
            return APIResponse.error("用户不存在", 404)
        
        return APIResponse.success(data={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return APIResponse.error(f"获取用户信息失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_user(
    request: UserCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        existing = db.query(AdminUser).filter(AdminUser.username == request.username).first()
        if existing:
            return APIResponse.error("用户名已存在", 400)
        
        user = AdminUser(
            id=f"USER-{uuid.uuid4().hex[:8].upper()}",
            username=request.username,
            password=request.password,
            role=request.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # 记录创建用户活动
        create_simple_activity(
            db=db,
            activity_type="user_create",
            message=f"创建新用户 '{user.username}'",
            user_id=current_user.id,
            target_id=user.id,
            target_type="user",
            details={
                "username": user.username,
                "role": user.role,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"User created: {user.id}")
        return APIResponse.success(data={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create user error: {e}")
        db.rollback()
        return APIResponse.error(f"创建用户失败: {str(e)}", 500)


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
        if not user:
            return APIResponse.error("用户不存在", 404)
        
        if request.username is not None:
            existing = db.query(AdminUser).filter(
                AdminUser.username == request.username,
                AdminUser.id != user_id
            ).first()
            if existing:
                return APIResponse.error("用户名已存在", 400)
            user.username = request.username
        
        if request.password is not None:
            user.password = request.password
        
        if request.role is not None:
            old_role = user.role
            user.role = request.role
            
            # 记录角色变更活动
            if old_role != request.role:
                record_role_change_activity(
                    db=db,
                    user_id=current_user.id,
                    target_user_id=user_id,
                    old_role=old_role,
                    new_role=request.role,
                    target_username=user.username,
                    operator_username=current_user.username
                )
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User updated: {user_id}")
        return APIResponse.success(data={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update user error: {e}")
        db.rollback()
        return APIResponse.error(f"更新用户失败: {str(e)}", 500)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        if user_id == current_user.id:
            return APIResponse.error("不能删除当前登录用户", 400)
        
        user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
        if not user:
            return APIResponse.error("用户不存在", 404)
        
        # 记录删除用户活动
        create_simple_activity(
            db=db,
            activity_type="user_delete",
            message=f"删除用户 '{user.username}'",
            user_id=current_user.id,
            target_id=user.id,
            target_type="user",
            details={
                "username": user.username,
                "role": user.role,
                "operator_username": current_user.username
            }
        )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"User deleted: {user_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        db.rollback()
        return APIResponse.error(f"删除用户失败: {str(e)}", 500)
