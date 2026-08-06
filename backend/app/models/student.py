from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    DateTime,
    text
)
from app.database.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    college_email = Column(String(150), unique=True, nullable=False)
    enrollment_no = Column(String(30), unique=True, nullable=False)
    mobile = Column(String(15))
    department = Column(String(50))
    year = Column(Integer)
    section = Column(String(10))
    password_hash = Column(String, nullable=False)
    reset_otp = Column(String, nullable=True)
    otp_created_at = Column(DateTime, nullable=True)
    trust_score = Column(Integer, default=100)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))