"""
Database schema for the Learning Management System
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/lms_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """User accounts table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="student")  # student, instructor, admin
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    progress_records = relationship("UserProgress", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
    code_submissions = relationship("CodeSubmission", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")

class Course(Base):
    """Courses table"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    language = Column(String(20), nullable=False)  # python, perl
    difficulty_level = Column(String(20), default="beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    progress_records = relationship("UserProgress", back_populates="course")

class UserProgress(Base):
    """User course progress tracking"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    module_id = Column(String(50))
    lesson_id = Column(String(50))
    progress_percentage = Column(Float, default=0.0)
    completed_at = Column(DateTime)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    time_spent_minutes = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    course = relationship("Course", back_populates="progress_records")

class QuizResult(Base):
    """Quiz results and scores"""
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_topic = Column(String(100), nullable=False)
    language = Column(String(20), nullable=False)
    difficulty = Column(String(20), default="beginner")
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score_percentage = Column(Float, nullable=False)
    time_taken_seconds = Column(Integer)
    questions_data = Column(JSON)  # Store quiz questions and answers
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_results")

class CodeSubmission(Base):
    """Code practice submissions and results"""
    __tablename__ = "code_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language = Column(String(20), nullable=False)
    code_content = Column(Text, nullable=False)
    execution_output = Column(Text)
    execution_error = Column(Text)
    execution_time_ms = Column(Integer)
    ai_feedback = Column(JSON)  # Store AI analysis feedback
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="code_submissions")

class ChatSession(Base):
    """AI chatbot conversations"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), nullable=False)
    language_focus = Column(String(20), default="python")
    messages = Column(JSON)  # Store conversation history
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")

class UserActivity(Base):
    """General user activity tracking"""
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # login, course_access, quiz_complete, etc.
    activity_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SystemSettings(Base):
    """System configuration and settings"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize tables
if __name__ == "__main__":
    create_tables()