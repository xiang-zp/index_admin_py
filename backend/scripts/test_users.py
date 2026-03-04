# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import AdminUser

db = SessionLocal()
try:
    users = db.query(AdminUser).all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}")
        print(f"Password (first 20 chars): {u.password[:20]}...")
finally:
    db.close()
