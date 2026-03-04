import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app.models.auth_location import AuthLocation

def create_table():
    try:
        AuthLocation.__table__.create(engine, checkfirst=True)
        print("✅ auth_locations 表创建成功！")
    except Exception as e:
        print(f"❌ 创建表失败: {e}")

if __name__ == "__main__":
    create_table()
