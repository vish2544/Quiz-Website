from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    role = Column(String, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    otp_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    attempts = Column(Integer, default=0)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, nullable=False)
    level = Column(String, nullable=False)
    type = Column(String, nullable=False)  # MCQ or Coding
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    testcases = Column(JSON, nullable=True)  # Only for coding questions
    options = Column(JSON, nullable=True)    # Only for MCQs
    answer = Column(String, nullable=True)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    code = Column(String, nullable=True)
    language = Column(String, nullable=True)
    score = Column(Integer, default=0)
    feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
