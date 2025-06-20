import streamlit as st
import pandas as pd
from typing import Dict, Optional

def initialize_session():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {
            # Default admin user for testing
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
