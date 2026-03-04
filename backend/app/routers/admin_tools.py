from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
import uuid
import os
import base64
from datetime import datetime, timedelta
from pathlib import Path

from app.database import get_db
from app.models.tool import Tool
from app.schemas.tool import ToolCreate, ToolUpdate
from app.utils.response import APIResponse
from app.utils.logger import get_logger
from app.utils.activity import create_simple_activity
from app.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()
logger = get_logger(__name__)
MAX_INLINE_IMAGE_LEN = 450000

IMAGE_DIR = Path(__file__).parent.parent.parent / "database" / "image"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

_tools_cache = None
_cache_time = None
_cache_ttl = timedelta(seconds=30)


def _generate_tool_id(db: Session) -> str:
    last_tool = db.query(Tool).order_by(Tool.id.desc()).first()
    if last_tool and last_tool.id.startswith("TOOL-"):
        try:
            last_num = int(last_tool.id.split("-")[1])
            new_num = last_num + 1
        except (ValueError, IndexError):
            new_num = 1
    else:
        new_num = 1
    return f"TOOL-{new_num:03d}"


def _save_image_to_file(tool_id: str, image_data: str) -> str | None:
    if not image_data:
        return None
    
    if image_data.startswith("http://") or image_data.startswith("https://"):
        return image_data
    
    if image_data.startswith("data:image"):
        try:
            header, base64_data = image_data.split(",", 1)
            if "png" in header:
                ext = "png"
            elif "gif" in header:
                ext = "gif"
            else:
                ext = "jpg"
            
            image_bytes = base64.b64decode(base64_data)
            filename = f"{tool_id}.{ext}"
            filepath = IMAGE_DIR / filename
            
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            return f"/database/image/{filename}"
        except Exception as e:
            logger.error(f"Save image error: {e}")
            return None
    
    return None


def _get_image_url(image_path: str | None, request) -> str:
    if not image_path:
        return ""
    
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path
    
    if image_path.startswith("/database/image/"):
        return f"http://{request.headers.get('host', 'localhost:8000')}{image_path}"
    
    return image_path


def _safe_image_for_response(image: str | None) -> str:
    if not image:
        return ""
    if image.startswith("http://") or image.startswith("https://"):
        return image
    if len(image) <= MAX_INLINE_IMAGE_LEN:
        return image
    return ""


@router.get("", response_model=dict)
async def get_tools(
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    global _tools_cache, _cache_time
    try:
        now = datetime.now()
        if _tools_cache and _cache_time and (now - _cache_time) < _cache_ttl:
            return APIResponse.success(data=_tools_cache)

        from sqlalchemy import case, literal_column

        tools = db.query(
            Tool.id,
            Tool.name,
            Tool.description,
            Tool.path,
            Tool.icon,
            Tool.row,
            Tool.is_visible,
            Tool.is_active,
            Tool.sort_order,
            Tool.created_at,
            Tool.updated_at,
            case(
                (Tool.image.like("http%"), Tool.image),
                (func.length(Tool.image) <= MAX_INLINE_IMAGE_LEN, Tool.image),
                else_=""
            ).label("image")
        ).order_by(Tool.id.desc()).all()

        result = []
        for tool in tools:
            result.append({
                "id": tool.id,
                "name": tool.name,
                "title": tool.name,
                "description": tool.description,
                "path": tool.path,
                "icon": tool.icon,
                "image": tool.image or "",
                "row": tool.row or "row1",
                "is_visible": tool.is_visible,
                "is_active": tool.is_active,
                "sort_order": tool.sort_order,
                "created_at": tool.created_at.isoformat() if tool.created_at else None,
                "updated_at": tool.updated_at.isoformat() if tool.updated_at else None
            })
        _tools_cache = result
        _cache_time = now
        return APIResponse.success(data=result)
    except Exception as e:
        logger.error(f"Get tools error: {e}")
        return APIResponse.error(f"获取项目列表失败: {str(e)}", 500)


@router.get("/{tool_id}", response_model=dict)
async def get_tool(
    tool_id: str,
    full_image: bool = False,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return APIResponse.error("项目不存在", 404)

        image = tool.image or ""
        if not full_image:
            image = _safe_image_for_response(image)

        return APIResponse.success(data={
            "id": tool.id,
            "name": tool.name,
            "title": tool.name,
            "description": tool.description,
            "path": tool.path,
            "icon": tool.icon,
            "image": image,
            "has_image": bool(tool.image),
            "image_truncated": bool(tool.image) and not bool(image),
            "is_visible": tool.is_visible,
            "is_active": tool.is_active,
            "sort_order": tool.sort_order,
            "created_at": tool.created_at.isoformat() if tool.created_at else None,
            "updated_at": tool.updated_at.isoformat() if tool.updated_at else None
        })
    except Exception as e:
        logger.error(f"Get tool error: {e}")
        return APIResponse.error(f"获取项目详情失败: {str(e)}", 500)

@router.post("", response_model=dict)
async def create_tool(
    request: ToolCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    global _tools_cache, _cache_time
    try:
        max_order = db.query(Tool).count()
        
        tool_name = request.title or request.name or "未命名项目"
        tool_id = _generate_tool_id(db)
        
        image_path = _save_image_to_file(tool_id, request.image) if request.image else None
        
        tool = Tool(
            id=tool_id,
            name=tool_name,
            title=request.title or tool_name,
            description=request.description,
            image=image_path,
            row=request.row or 'row1',
            is_visible=request.is_visible,
            sort_order=max_order
        )
        db.add(tool)
        db.commit()
        db.refresh(tool)
        
        create_simple_activity(
            db=db,
            activity_type="tool_create",
            message=f"创建开源项目 '{tool.name}'",
            user_id=current_user.id,
            target_id=tool.id,
            target_type="tool",
            details={
                "title": tool.name,
                "operator_username": current_user.username
            }
        )
        
        _tools_cache = None
        _cache_time = None
        
        logger.info(f"Tool created: {tool.id}")
        return APIResponse.success(data={
            "id": tool.id,
            "name": tool.name,
            "title": tool.name,
            "description": tool.description,
            "path": tool.path,
            "icon": tool.icon,
            "image": tool.image or "",
            "row": tool.row or "row1",
            "has_image": bool(tool.image),
            "is_visible": tool.is_visible,
            "is_active": tool.is_active,
            "sort_order": tool.sort_order,
            "created_at": tool.created_at.isoformat() if tool.created_at else None,
            "updated_at": tool.updated_at.isoformat() if tool.updated_at else None
        })
    except Exception as e:
        logger.error(f"Create tool error: {e}")
        db.rollback()
        return APIResponse.error(f"创建项目失败: {str(e)}", 500)


@router.put("/{tool_id}", response_model=dict)
async def update_tool(
    tool_id: str,
    request: ToolUpdate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    global _tools_cache, _cache_time
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return APIResponse.error("项目不存在", 404)
        
        if request.title is not None:
            tool.name = request.title
            tool.title = request.title
        elif request.name is not None:
            tool.name = request.name
            tool.title = request.name
        if request.description is not None:
            tool.description = request.description
        if request.image is not None:
            image_path = _save_image_to_file(tool_id, request.image)
            tool.image = image_path
        if request.row is not None:
            tool.row = request.row
        if request.is_visible is not None:
            tool.is_visible = request.is_visible
        
        db.commit()
        db.refresh(tool)
        
        create_simple_activity(
            db=db,
            activity_type="tool_update",
            message=f"更新开源项目 '{tool.name}'",
            user_id=current_user.id,
            target_id=tool.id,
            target_type="tool",
            details={
                "title": tool.name,
                "operator_username": current_user.username
            }
        )
        
        _tools_cache = None
        _cache_time = None
        
        logger.info(f"Tool updated: {tool_id}")
        return APIResponse.success(data={
            "id": tool.id,
            "name": tool.name,
            "title": tool.name,
            "description": tool.description,
            "path": tool.path,
            "icon": tool.icon,
            "image": tool.image or "",
            "row": tool.row or "row1",
            "has_image": bool(tool.image),
            "is_visible": tool.is_visible,
            "is_active": tool.is_active,
            "sort_order": tool.sort_order,
            "created_at": tool.created_at.isoformat() if tool.created_at else None,
            "updated_at": tool.updated_at.isoformat() if tool.updated_at else None
        })
    except Exception as e:
        logger.error(f"Update tool error: {e}")
        db.rollback()
        return APIResponse.error(f"更新项目失败: {str(e)}", 500)


@router.delete("/{tool_id}", response_model=dict)
async def delete_tool(
    tool_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    global _tools_cache, _cache_time
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return APIResponse.error("项目不存在", 404)
        
        # 记录删除开源项目活动
        create_simple_activity(
            db=db,
            activity_type="tool_delete",
            message=f"删除开源项目 '{tool.name}'",
            user_id=current_user.id,
            target_id=tool.id,
            target_type="tool",
            details={
                "title": tool.name,
                "operator_username": current_user.username
            }
        )
        
        db.delete(tool)
        db.commit()
        
        _tools_cache = None
        _cache_time = None
        
        logger.info(f"Tool deleted: {tool_id}")
        return APIResponse.success(message="删除成功")
    except Exception as e:
        logger.error(f"Delete tool error: {e}")
        db.rollback()
        return APIResponse.error(f"删除项目失败: {str(e)}", 500)


@router.patch("/{tool_id}/toggle_visibility", response_model=dict)
async def toggle_tool_visibility(
    tool_id: str,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    global _tools_cache, _cache_time
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return APIResponse.error("项目不存在", 404)
        
        tool.is_visible = not tool.is_visible
        db.commit()
        
        # 记录切换开源项目可见性活动
        create_simple_activity(
            db=db,
            activity_type="tool_toggle",
            message=f"设置开源项目 '{tool.name}' 为 {'显示' if tool.is_visible else '隐藏'}",
            user_id=current_user.id,
            target_id=tool.id,
            target_type="tool",
            details={
                "title": tool.name,
                "is_visible": tool.is_visible,
                "operator_username": current_user.username
            }
        )
        
        _tools_cache = None
        _cache_time = None
        
        logger.info(f"Tool visibility toggled: {tool_id} -> {tool.is_visible}")
        return APIResponse.success(message="状态切换成功")
    except Exception as e:
        logger.error(f"Toggle tool visibility error: {e}")
        db.rollback()
        return APIResponse.error(f"切换状态失败: {str(e)}", 500)
