from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.auth_code import AuthCode
from app.schemas.auth_code import AuthCodeCreate, AuthCodeUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_auth_codes(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_codes = db.query(AuthCode).order_by(AuthCode.created_at.desc()).all()
        return APIResponse.success(data=[
            {
                "id": ac.id,
                "description": ac.description,
                "invite_code": ac.invite_code,
                "status": ac.status,
                "auth_location": ac.auth_location,
                "authorized_user": ac.authorized_user,
                "authorized_at": ac.authorized_at.isoformat() if ac.authorized_at else None,
                "expire_time": ac.expire_time.isoformat() if ac.expire_time else None,
                "created_at": ac.created_at.isoformat() if ac.created_at else None,
                "updated_at": ac.updated_at.isoformat() if ac.updated_at else None
            }
            for ac in auth_codes
        ])
    except Exception as e:
        logger.error(f"Get auth codes error: {e}")
        return APIResponse.error(f"获取授权码列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_auth_code(
    request: AuthCodeCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        existing = db.query(AuthCode).filter(AuthCode.invite_code == request.invite_code).first()
        if existing:
            return APIResponse.error("授权码已存在", 400)
        
        expire_time = None
        if request.end_date:
            try:
                expire_time = datetime.fromisoformat(request.end_date)
            except ValueError:
                return APIResponse.error("end_date 格式错误，应为 ISO 8601 格式", 400)
        
        auth_code = AuthCode(
            id=f"AUTH-{uuid.uuid4().hex[:8].upper()}",
            description=request.description,
            invite_code=request.invite_code,
            auth_location=request.auth_location,
            status="authorized",
            expire_time=expire_time
        )
        db.add(auth_code)
        db.commit()
        db.refresh(auth_code)
        
        # 记录创建授权码活动
        create_simple_activity(
            db=db,
            activity_type="auth_code_create",
            message=f"创建授权码 '{auth_code.invite_code}'",
            user_id=current_user.id,
            target_id=auth_code.id,
            target_type="auth_code",
            details={
                "invite_code": auth_code.invite_code,
                "description": auth_code.description,
                "auth_location": auth_code.auth_location,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Auth code created: {auth_code.id}")
        return APIResponse.success(data={
            "id": auth_code.id,
            "description": auth_code.description,
            "invite_code": auth_code.invite_code,
            "status": auth_code.status,
            "auth_location": auth_code.auth_location,
            "authorized_user": auth_code.authorized_user,
            "authorized_at": auth_code.authorized_at.isoformat() if auth_code.authorized_at else None,
            "expire_time": auth_code.expire_time.isoformat() if auth_code.expire_time else None,
            "created_at": auth_code.created_at.isoformat() if auth_code.created_at else None,
            "updated_at": auth_code.updated_at.isoformat() if auth_code.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create auth code error: {e}")
        db.rollback()
        return APIResponse.error(f"创建授权码失败: {str(e)}", 500)


@router.put("/{auth_code_id}", response_model=dict)
async def update_auth_code(
    auth_code_id: str,
    request: AuthCodeUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_code = db.query(AuthCode).filter(AuthCode.id == auth_code_id).first()
        if not auth_code:
            return APIResponse.error("授权码不存在", 404)
        
        if request.description is not None:
            auth_code.description = request.description
        if request.auth_location is not None:
            auth_code.auth_location = request.auth_location
        if request.status is not None:
            auth_code.status = request.status
        if request.expire_time is not None:
            try:
                auth_code.expire_time = datetime.fromisoformat(request.expire_time)
            except ValueError:
                return APIResponse.error("expire_time 格式错误，应为 ISO 8601 格式", 400)
        
        db.commit()
        db.refresh(auth_code)
        
        # 记录更新授权码活动
        create_simple_activity(
            db=db,
            activity_type="auth_code_update",
            message=f"更新授权码 '{auth_code.invite_code}'",
            user_id=current_user.id,
            target_id=auth_code.id,
            target_type="auth_code",
            details={
                "invite_code": auth_code.invite_code,
                "description": auth_code.description,
                "auth_location": auth_code.auth_location,
                "status": auth_code.status,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Auth code updated: {auth_code_id}")
        return APIResponse.success(data={
            "id": auth_code.id,
            "description": auth_code.description,
            "invite_code": auth_code.invite_code,
            "status": auth_code.status,
            "auth_location": auth_code.auth_location,
            "authorized_user": auth_code.authorized_user,
            "authorized_at": auth_code.authorized_at.isoformat() if auth_code.authorized_at else None,
            "expire_time": auth_code.expire_time.isoformat() if auth_code.expire_time else None,
            "created_at": auth_code.created_at.isoformat() if auth_code.created_at else None,
            "updated_at": auth_code.updated_at.isoformat() if auth_code.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update auth code error: {e}")
        db.rollback()
        return APIResponse.error(f"更新授权码失败: {str(e)}", 500)


@router.delete("/{auth_code_id}", response_model=dict)
async def delete_auth_code(
    auth_code_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_code = db.query(AuthCode).filter(AuthCode.id == auth_code_id).first()
        if not auth_code:
            return APIResponse.error("授权码不存在", 404)
        
        # 记录删除授权码活动
        create_simple_activity(
            db=db,
            activity_type="auth_code_delete",
            message=f"删除授权码 '{auth_code.invite_code}'",
            user_id=current_user.id,
            target_id=auth_code.id,
            target_type="auth_code",
            details={
                "invite_code": auth_code.invite_code,
                "description": auth_code.description,
                "auth_location": auth_code.auth_location,
                "operator_username": current_user.username
            }
        )
        
        db.delete(auth_code)
        db.commit()
        
        logger.info(f"Auth code deleted: {auth_code_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete auth code error: {e}")
        db.rollback()
        return APIResponse.error(f"删除授权码失败: {str(e)}", 500)


@router.post("/{auth_code_id}/revoke", response_model=dict)
async def revoke_auth_code(
    auth_code_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_code = db.query(AuthCode).filter(AuthCode.id == auth_code_id).first()
        if not auth_code:
            return APIResponse.error("授权码不存在", 404)
        
        auth_code.status = "revoked"
        db.commit()
        
        # 记录撤销授权码活动
        create_simple_activity(
            db=db,
            activity_type="auth_code_revoke",
            message=f"撤销授权码 '{auth_code.invite_code}'",
            user_id=current_user.id,
            target_id=auth_code.id,
            target_type="auth_code",
            details={
                "invite_code": auth_code.invite_code,
                "description": auth_code.description,
                "auth_location": auth_code.auth_location,
                "operator_username": current_user.username
            }
        )
        
        logger.info(f"Auth code revoked: {auth_code_id}")
        return APIResponse.success(message="授权已撤销")
    except Exception as e:
        logger.error(f"Revoke auth code error: {e}")
        db.rollback()
        return APIResponse.error(f"撤销授权失败: {str(e)}", 500)
