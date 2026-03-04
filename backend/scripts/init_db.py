import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database import Base
from app.models import AdminUser, Agent, Tool, Document, Review, AuthCode, AuthLocation, Carousel, FooterConfig, FooterLink, Activity, DocumentCategory
from app.utils.auth import get_password_hash
import uuid

def create_database():
    db_url = settings.DATABASE_URL
    db_name = db_url.split("/")[-1]
    base_url = db_url.rsplit("/", 1)[0]
    
    engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
    
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"Database '{db_name}' created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    finally:
        engine.dispose()
    
    return True

def create_tables():
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        engine.dispose()
    
    return True

def create_initial_data():
    from app.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        existing_admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not existing_admin:
            admin = AdminUser(
                id=f"USER-{uuid.uuid4().hex[:8].upper()}",
                username="admin",
                password="admin123",
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Default admin user created: admin / admin123")
        else:
            print("Admin user already exists.")
        
        footer_config = db.query(FooterConfig).first()
        if not footer_config:
            footer_config = FooterConfig(
                id=1,
                logo_url="/assets/WechatIMG100.jpg",
                slogan="智能搜索助手，为您提供精准、高效的信息检索服务。"
            )
            db.add(footer_config)
            db.commit()
            print("Default footer config created.")
        
        agents_count = db.query(Agent).count()
        if agents_count == 0:
            agents = [
                Agent(id=f"AGENT-{uuid.uuid4().hex[:8].upper()}", name="xx1-智能体", api="https://api.coze.com/v1/chat", source="内置", bot_id="7348xxxxxx", is_visible=True, sort_order=0),
                Agent(id=f"AGENT-{uuid.uuid4().hex[:8].upper()}", name="xx2-智能体", api="https://api.coze.com/v1/chat", source="内置", bot_id="7348yyyyyy", is_visible=True, sort_order=1),
                Agent(id=f"AGENT-{uuid.uuid4().hex[:8].upper()}", name="xx3-智能体", api="https://api.coze.com/v1/chat", source="内置", bot_id="7348zzzzzz", is_visible=True, sort_order=2),
            ]
            db.add_all(agents)
            db.commit()
            print("Default agents created.")
        
        tools_count = db.query(Tool).count()
        if tools_count == 0:
            tools = [
                Tool(id=f"TOOL-{uuid.uuid4().hex[:8].upper()}", title="Python爬虫工具", description="强大的Python爬虫工具，支持多种网站抓取", image="https://img02.mockplus.cn/image/2024-12-31/47efe140-c757-11ef-b7cd-d5492e1eb796.png", is_visible=True, sort_order=0),
                Tool(id=f"TOOL-{uuid.uuid4().hex[:8].upper()}", title="自动化测试框架", description="基于Python的自动化测试框架，支持Web和API测试", image="https://img02.mockplus.cn/image/2023-09-12/616e4d00-5156-11ee-be47-bb0fa8736eee.png", is_visible=True, sort_order=1),
                Tool(id=f"TOOL-{uuid.uuid4().hex[:8].upper()}", title="数据分析工具", description="高效的数据分析工具，支持多种数据格式", image="https://img02.mockplus.cn/image/2023-09-01/3dd230a0-489b-11ee-9149-31084acae451.png", is_visible=True, sort_order=2),
            ]
            db.add_all(tools)
            db.commit()
            print("Default tools created.")
        
        carousels_count = db.query(Carousel).count()
        if carousels_count == 0:
            carousels = [
                Carousel(id=f"CAR-{uuid.uuid4().hex[:8].upper()}", title="欢迎使用智能助手", description="为您提供精准、高效的信息检索服务", is_visible=True, sort_order=0),
                Carousel(id=f"CAR-{uuid.uuid4().hex[:8].upper()}", title="AI 驱动的精准信息检索", description="支持多种智能体切换", is_visible=True, sort_order=1),
                Carousel(id=f"CAR-{uuid.uuid4().hex[:8].upper()}", title="实时对话与智能问答", description="智能问答，快速响应", is_visible=True, sort_order=2),
            ]
            db.add_all(carousels)
            db.commit()
            print("Default carousels created.")
        
        print("Initial data setup completed.")
        
    except Exception as e:
        print(f"Error creating initial data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("=" * 50)
    print("Starting database initialization...")
    print("=" * 50)
    
    if create_database():
        print("\n[1/3] Database created successfully.")
    else:
        print("\n[1/3] Failed to create database.")
        return
    
    if create_tables():
        print("[2/3] Tables created successfully.")
    else:
        print("[2/3] Failed to create tables.")
        return
    
    create_initial_data()
    print("[3/3] Initial data created successfully.")
    
    print("\n" + "=" * 50)
    print("Database initialization completed!")
    print("=" * 50)
    print("\nDefault admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPlease change the default password after first login!")

if __name__ == "__main__":
    main()
