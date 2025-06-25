from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from db import engine


Base = declarative_base()

class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True)
   username = Column(String)
   email = Column(String, unique=True)
   hashed_password = Column(String)
   create_time = Column(DateTime, default=datetime.now)
   predictions = relationship("Predictions", back_populates="user")

class Predictions(Base):
   __tablename__ = "predictions"
   id = Column(Integer, primary_key=True)
   user_id = Column(Integer, ForeignKey("users.id"))
   response = Column(Text)
   sender = Column(String)
   timestamp = Column(DateTime, default=datetime.now)
   user = relationship("User", back_populates="predictions")

class OtpStore(Base):
    __tablename__ = "otp_store"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    otp = Column(String)
    expire_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)