from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.carousel import Carousel
from app.utils.response import APIResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=dict)
async def get_carousels(db: Session = Depends(get_db)):
    """
    获取滚动消息列表（公开接口）
    """
    try:
        carousels = db.query(Carousel).filter(
            Carousel.is_visible == True
        ).order_by(Carousel.sort_order).all()
        
        # 返回 description 而不是 title，因为用户实际输入的内容在 description 中
        messages = [c.description if c.description else c.title for c in carousels]
        
        return APIResponse.success(data=messages)
        
    except Exception as e:
        logger.error(f"Get carousels error: {e}")
        return APIResponse.error(f"获取滚动消息失败: {str(e)}", 500)
