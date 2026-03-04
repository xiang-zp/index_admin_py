from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

password = "Root@123456"
encoded_password = quote_plus(password)
DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@115.190.98.26:3306/smart_qa"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        conn.execute(text('ALTER TABLE tools MODIFY COLUMN title VARCHAR(100) NULL'))
        conn.commit()
        print('Column title modified to allow NULL successfully')
    except Exception as e:
        print(f'Error: {e}')
