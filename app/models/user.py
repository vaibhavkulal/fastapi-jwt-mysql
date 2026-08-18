from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, text

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="USER", server_default=text("'USER'"))
    created_at = Column(DateTime, default=datetime.utcnow)