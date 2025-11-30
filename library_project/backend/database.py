# Tệp: database.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

# Cấu hình Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend/library.db"

# Khởi tạo Engine tạo kết nối đến database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Khởi tạo Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Khởi tạo Base cho các mô hình SQLAlchemy
Base = declarative_base()

# Dependency: Hàm để lấy và đóng session DB
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()