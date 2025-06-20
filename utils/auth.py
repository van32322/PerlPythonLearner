import streamlit as st
import pandas as pd
import hashlib
from typing import Dict, Optional
from sqlalchemy.orm import Session
from utils.db_schema import User, SessionLocal
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def create_user(username: str, email: str, password: str, role: str = "student") -> bool:
    """Create new user in database"""
    try:
        with SessionLocal() as db:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return False
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role=role,
                created_at=datetime.utcnow()
            )
            
            db.add(new_user)
            db.commit()
            return True
            
    except Exception as e:
        st.error(f"Error creating user: {str(e)}")
        return False

def authenticate_user_db(username: str, password: str) -> Optional[Dict]:
    """Authenticate user against database"""
    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            
            if user and verify_password(password, user.password_hash):
                # Update last login
                db.query(User).filter(User.id == user.id).update({
                    User.last_login: datetime.utcnow()
                })
                db.commit()
                
                return {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'full_name': user.full_name,
                    'created_at': user.created_at,
                    'last_login': user.last_login
                }
        return None
        
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None

def initialize_session():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Create default admin user if database is available
    try:
        with SessionLocal() as db:
            admin_user = db.query(User).filter(User.username == 'admin').first()
            if not admin_user:
                create_user('admin', 'admin@example.com', 'admin123', 'instructor')
    except:
        # Fallback to session-based storage
        if 'users_db' not in st.session_state:
            st.session_state.users_db = {
                'admin': {
                    'email': 'admin@example.com',
                    'password': 'admin123',
                    'role': 'instructor',
                    'created_at': pd.Timestamp.now(),
                    'profile': {
                        'bio': 'Platform Administrator',
                        'learning_goals': [],
                        'preferred_language': 'python'
                    }
                }
            }
    
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'lessons_completed': 0,
            'exercises_completed': 0,
            'average_quiz_score': 0.0,
            'learning_streak': 0,
            'completed_courses': [],
            'current_courses': [],
            'skill_levels': {
                'python': 'beginner',
                'perl': 'beginner'
            }
        }

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user() -> Optional[Dict]:
    """Get current authenticated user data"""
    if check_authentication():
        return st.session_state.user_data
    return None

def is_instructor() -> bool:
    """Check if current user is an instructor"""
    user = get_current_user()
    return user and user.get('role') == 'instructor'

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.rerun()

def update_user_progress(progress_type: str, increment: int = 1):
    """Update user progress metrics"""
    if progress_type in st.session_state.user_progress:
        if progress_type in ['lessons_completed', 'exercises_completed', 'learning_streak']:
            st.session_state.user_progress[progress_type] += increment
        elif progress_type == 'average_quiz_score':
            # For quiz scores, we need to handle averaging
            current_score = st.session_state.user_progress.get('average_quiz_score', 0)
            quiz_count = st.session_state.user_progress.get('quiz_count', 0)
            new_score = ((current_score * quiz_count) + increment) / (quiz_count + 1)
            st.session_state.user_progress['average_quiz_score'] = new_score
            st.session_state.user_progress['quiz_count'] = quiz_count + 1

def get_user_skill_level(language: str) -> str:
    """Get user's skill level for a specific programming language"""
    return st.session_state.user_progress.get('skill_levels', {}).get(language.lower(), 'beginner')

def update_skill_level(language: str, level: str):
    """Update user's skill level for a programming language"""
    if 'skill_levels' not in st.session_state.user_progress:
        st.session_state.user_progress['skill_levels'] = {}
    st.session_state.user_progress['skill_levels'][language.lower()] = level
