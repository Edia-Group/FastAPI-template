from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Integer
from database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    phone_number = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)

class OTP(Base):
    __tablename__ = "otps"
    phone_number = Column(String, primary_key=True)
    otp = Column(String)
    timestamp = Column(DateTime)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_phone_number = Column(String, ForeignKey("users.phone_number"))
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="posts")