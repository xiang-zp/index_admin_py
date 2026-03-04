from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.auth_location import AuthLocation
from app.schemas.auth_location import AuthLocationCreate, AuthLocationUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=dict)
async def get_auth_locations(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_locations = db.query(AuthLocation).order_by(AuthLocation.created_at.desc()).all()
        return APIResponse.success(data=[
            {
                "id": al.id,
                "value": al.value,
                "label": al.label,
                "description": al.description,
                "created_at": al.created_at.isoformat() if al.created_at else None,
                "updated_at": al.updated_at.isoformat() if al.updated_at else None
            }
            for al in auth_locations
        ])
    except Exception as e:
        logger.error(f"Get auth locations error: {e}")
        return APIResponse.error(f"获取授权位置列表失败: {str(e)}", 500)


@router.post("", response_model=dict)
async def create_auth_location(
    request: AuthLocationCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        existing = db.query(AuthLocation).filter(AuthLocation.value == request.value).first()
        if existing:
            return APIResponse.error("授权位置已存在", 400)
        
        auth_location = AuthLocation(
            id=f"LOC-{uuid.uuid4().hex[:8].upper()}",
            value=request.value,
            label=request.label,
            description=request.description
        )
        db.add(auth_location)
        db.commit()
        db.refresh(auth_location)
        
        logger.info(f"Auth location created: {auth_location.id}")
        return APIResponse.success(data={
            "id": auth_location.id,
            "value": auth_location.value,
            "label": auth_location.label,
            "description": auth_location.description,
            "created_at": auth_location.created_at.isoformat() if auth_location.created_at else None,
            "updated_at": auth_location.updated_at.isoformat() if auth_location.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create auth location error: {e}")
        db.rollback()
        return APIResponse.error(f"创建授权位置失败: {str(e)}", 500)


@router.delete("/{location_id}", response_model=dict)
async def delete_auth_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        auth_location = db.query(AuthLocation).filter(AuthLocation.id == location_id).first()
        if not auth_location:
            return APIResponse.error("授权位置不存在", 404)
        
        db.delete(auth_location)
        db.commit()
        
        logger.info(f"Auth location deleted: {location_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete auth location error: {e}")
        db.rollback()
        return APIResponse.error(f"删除授权位置失败: {str(e)}", 500)
