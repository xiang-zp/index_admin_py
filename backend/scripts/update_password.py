import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import AdminUser

def update_passwords():
    db = SessionLocal()
    
    try:
        users = db.query(AdminUser).all()
        
        for user in users:
            print(f"Updating password for user: {user.username}")
            print(f"Current password: {user.password}")
            
            if user.password.startswith('$2b$'):
                print("Password is hashed, updating to plain text...")
                if user.username == "admin":
                    user.password = "admin123"
                else:
                    user.password = "123456"
                print(f"New password (plain): {user.password}")
        
        db.commit()
        print("\nAll passwords updated successfully!")
        
    except Exception as e:
        print(f"Error updating passwords: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_passwords()
