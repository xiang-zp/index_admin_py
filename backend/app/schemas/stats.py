from pydantic import BaseModel


class Stats(BaseModel):
    """统计数据"""
    total_users: int
    total_conversations: int
    total_tools_used: int
    avg_rating: float
