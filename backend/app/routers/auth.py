from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.user import AdminUser
from app.models.auth_code import AuthCode
from app.schemas.auth import LoginRequest, LoginResponse, UserInfo, UserProfile
from app.utils.auth import verify_password, get_password_hash, create_access_token
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.dependencies import get_current_user

router = APIRouter()
logger = get_logger(__name__)


class VerifyCodeRequest(BaseModel):
    invite_code: str


@router.post("/verify", response_model=dict)
async def verify_invite_code(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db)
):
    try:
        auth_code = db.query(AuthCode).filter(AuthCode.invite_code == request.invite_code).first()
        
        if not auth_code:
            return APIResponse.error("授权码不存在", 404)
        
        if auth_code.status == "revoked":
            return APIResponse.error("该授权码已被撤销", 400)
        
        if auth_code.expire_time and auth_code.expire_time < datetime.now():
            return APIResponse.error("该授权码已过期", 400)
        
        return APIResponse.success(data={
            "is_authorized": True,
            "expire_time": auth_code.expire_time.isoformat() if auth_code.expire_time else None,
            "auth_location": auth_code.auth_location,
            "description": auth_code.description
        })
        
    except Exception as e:
        logger.error(f"Verify invite code error: {e}")
        return APIResponse.error(f"验证失败: {str(e)}", 500)


@router.post("/revoke", response_model=dict)
async def revoke_current_authorization(
    db: Session = Depends(get_db)
):
    try:
        return APIResponse.success(data={
            "is_authorized": False
        })
    except Exception as e:
        logger.error(f"Revoke error: {e}")
        return APIResponse.error(f"撤销失败: {str(e)}", 500)


@router.post("/admin/login", response_model=dict)
async def admin_login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(AdminUser).filter(AdminUser.username == request.username).first()
        
        if not user:
            return APIResponse.error("用户名或密码错误", 401)
        
        if request.password != user.password:
            return APIResponse.error("用户名或密码错误", 401)
        
        user.last_login_at = datetime.now()
        db.commit()
        
        token = create_access_token({"sub": user.id})
        
        logger.info(f"Admin login: {user.username}")
        
        return APIResponse.success(
            data={
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return APIResponse.error(f"登录失败: {str(e)}", 500)


@router.post("/admin/logout", response_model=dict)
async def admin_logout(
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        logger.info(f"Admin logout: {current_user.username}")
        return APIResponse.success(message="登出成功")
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return APIResponse.error(f"登出失败: {str(e)}", 500)


@router.get("/admin/profile", response_model=dict)
async def get_admin_profile(
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        return APIResponse.success(
            data={
                "id": current_user.id,
                "username": current_user.username,
                "role": current_user.role,
                "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
                "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None
            }
        )
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return APIResponse.error(f"获取用户信息失败: {str(e)}", 500)
