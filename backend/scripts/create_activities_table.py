import sys
import os

# 切换到backend目录以确保.env文件正确加载
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.config import settings
from app.models.activity import Activity

def create_table():
    try:
        # 使用配置中的数据库URL创建引擎
        engine = create_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            pool_pre_ping=True
        )
        print(f"正在连接到数据库: {settings.DATABASE_URL}")
        Activity.__table__.create(engine, checkfirst=True)
        print("✅ activities 表创建成功！")
    except Exception as e:
        print(f"❌ 创建表失败: {e}")

if __name__ == "__main__":
    create_table()