from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tool import Tool
from app.schemas.tool import ToolResponse
from app.utils.response import APIResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=dict)
async def get_tools(db: Session = Depends(get_db)):
    """
    获取工具列表
    """
    try:
        tools = db.query(Tool).filter(Tool.is_active == True, Tool.is_visible == True).order_by(Tool.sort_order).all()
        
        tool_list = [
            ToolResponse(
                id=tool.id,
                name=tool.name,
                description=tool.description,
                path=tool.path,
                icon=tool.icon,
                image=tool.image,
                row=tool.row,
                is_visible=tool.is_visible,
                is_active=tool.is_active,
                sort_order=tool.sort_order,
                created_at=tool.created_at,
                updated_at=tool.updated_at
            )
            for tool in tools
        ]
        
        return APIResponse.success(data=tool_list)
        
    except Exception as e:
        logger.error(f"Error getting tools: {e}")
        return APIResponse.error(f"获取工具列表失败: {str(e)}", 500)
