from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import UserAuthorization
from app.models.conversation import Conversation
from app.models.review import Review
from app.schemas.stats import Stats
from app.utils.response import APIResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=dict)
async def get_stats(db: Session = Depends(get_db)):
    """
    获取统计数据
    """
    try:
        # 获取授权用户数
        total_users = db.query(UserAuthorization).filter(
            UserAuthorization.is_authorized == True
        ).count()
        
        # 获取对话数
        total_conversations = db.query(Conversation).count()
        
        # 工具使用次数（这里用对话数模拟）
        total_tools_used = total_conversations * 2
        
        # 获取平均评分
        avg_rating_result = db.query(func.avg(Review.rating)).scalar()
        avg_rating = round(avg_rating_result, 1) if avg_rating_result else 0.0
        
        stats_data = Stats(
            total_users=total_users if total_users > 0 else 1000,  # 默认值
            total_conversations=total_conversations if total_conversations > 0 else 5000,  # 默认值
            total_tools_used=total_tools_used if total_tools_used > 0 else 20000,  # 默认值
            avg_rating=avg_rating if avg_rating > 0 else 4.8  # 默认值
        )
        
        return APIResponse.success(data=stats_data)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return APIResponse.error(f"获取统计数据失败: {str(e)}", 500)
