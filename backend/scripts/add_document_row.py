"""
添加 documents 表的 row 字段，删除 date 字段
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

def migrate_document_fields():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN `row` VARCHAR(10) DEFAULT 'row1' NOT NULL COMMENT '展示位：row1第一行，row2第二行'"))
            conn.commit()
            print("成功添加 row 字段")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("row 字段已存在，跳过")
            else:
                print(f"添加 row 字段失败: {e}")
        
        try:
            conn.execute(text("ALTER TABLE documents DROP COLUMN date"))
            conn.commit()
            print("成功删除 date 字段")
        except Exception as e:
            if "check that column/key exists" in str(e) or "Unknown column" in str(e):
                print("date 字段不存在，跳过")
            else:
                print(f"删除 date 字段失败: {e}")

if __name__ == "__main__":
    migrate_document_fields()
