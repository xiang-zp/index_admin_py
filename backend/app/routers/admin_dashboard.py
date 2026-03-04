from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.user import AdminUser
from app.models.agent import Agent
from app.models.tool import Tool
from app.models.document import Document
from app.models.review import Review
from app.models.activity import Activity
from app.schemas.dashboard import ActivityResponse
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.dependencies import get_current_user

router = APIRouter()
logger = get_logger(__name__)


@router.get("/stats", response_model=dict)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        agents_count = db.query(Agent).count()
        tools_count = db.query(Tool).count()
        documents_count = db.query(Document).count()
        reviews_count = db.query(Review).count()
        users_count = db.query(AdminUser).count()
        
        return APIResponse.success(data={
            "agents": agents_count,
            "tools": tools_count,
            "documents": documents_count,
            "reviews": reviews_count,
            "users": users_count
        })
    except Exception as e:
        logger.error(f"Get dashboard stats error: {e}")
        return APIResponse.error(f"获取统计数据失败: {str(e)}", 500)


@router.get("/activities", response_model=dict)
async def get_dashboard_activities(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        # 从Activity表查询最新的活动记录
        activities = db.query(Activity).order_by(Activity.created_at.desc()).limit(limit).all()
        
        # 获取所有相关的用户名
        user_ids = set(a.user_id for a in activities if a.user_id)
        users = {}
        if user_ids:
            admin_users = db.query(AdminUser).filter(AdminUser.id.in_(user_ids)).all()
            users = {u.id: u.username for u in admin_users}
        
        # 转换为响应格式
        activity_list = []
        for idx, activity in enumerate(activities):
            username = users.get(activity.user_id, '未知用户') if activity.user_id else '系统'
            activity_list.append({
                "id": idx + 1,  # 前端需要连续的数字ID
                "db_id": activity.id,  # 数据库实际ID，用于删除操作
                "type": activity.type,
                "message": activity.message,
                "time": activity.created_at.isoformat(),
                "user_id": activity.user_id,
                "username": username,
                "target_id": activity.target_id,
                "target_type": activity.target_type
            })
        
        return APIResponse.success(data=activity_list)
    except Exception as e:
        logger.error(f"Get dashboard activities error: {e}")
        return APIResponse.error(f"获取活动记录失败: {str(e)}", 500)


@router.delete("/activities/all")
async def delete_all_activities(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        # 查询所有活动记录数量用于日志
        total_count = db.query(Activity).count()
        
        if total_count == 0:
            return APIResponse.success(message="没有活动记录可删除", data={"deleted_count": 0})
        
        # 删除所有活动记录
        deleted_count = db.query(Activity).delete()
        db.commit()
        
        logger.info(f"所有活动记录已删除: 共{deleted_count}条, 操作人: {current_user.username}")
        return APIResponse.success(
            message=f"成功删除所有活动记录 ({deleted_count} 条)",
            data={"deleted_count": deleted_count}
        )
    except Exception as e:
        db.rollback()
        logger.error(f"删除所有活动记录错误: {e}")
        return APIResponse.error(f"删除所有活动记录失败: {str(e)}", 500)


@router.delete("/activities/{activity_id}")
async def delete_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        # 查找要删除的活动记录
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return APIResponse.error(f"活动记录不存在: {activity_id}", 404)
        
        # 删除记录
        db.delete(activity)
        db.commit()
        
        logger.info(f"活动记录已删除: {activity_id}, 操作人: {current_user.username}")
        return APIResponse.success(message="活动记录删除成功")
    except Exception as e:
        db.rollback()
        logger.error(f"删除活动记录错误: {e}")
        return APIResponse.error(f"删除活动记录失败: {str(e)}", 500)
