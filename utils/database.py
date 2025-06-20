import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import json
from datetime import datetime

def initialize_database():
    """Initialize the session-based database"""
    if 'db_initialized' not in st.session_state:
        st.session_state.db_initialized = True
        
        # User progress tracking
        if 'user_activities' not in st.session_state:
            st.session_state.user_activities = []
        
        # Quiz results
        if 'quiz_results' not in st.session_state:
            st.session_state.quiz_results = []
        
        # Code submissions
        if 'code_submissions' not in st.session_state:
            st.session_state.code_submissions = []
        
        # Course evaluations
        if 'course_evaluations' not in st.session_state:
            st.session_state.course_evaluations = []

def log_user_activity(activity_type: str, details: Dict):
    """Log user activity for progress tracking"""
    if 'user_activities' not in st.session_state:
        st.session_state.user_activities = []
    
    activity = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('user_data', {}).get('username', 'anonymous'),
        'activity_type': activity_type,
        'details': details
    }
    
    st.session_state.user_activities.append(activity)

def save_quiz_result(quiz_data: Dict):
    """Save quiz result to database"""
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = []
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('user_data', {}).get('username', 'anonymous'),
        'quiz_topic': quiz_data.get('topic', ''),
        'language': quiz_data.get('language', ''),
        'score': quiz_data.get('score', 0),
        'total_questions': quiz_data.get('total_questions', 0),
        'time_taken': quiz_data.get('time_taken', 0),
        'answers': quiz_data.get('answers', [])
    }
    
    st.session_state.quiz_results.append(result)

def save_code_submission(code_data: Dict):
    """Save code submission to database"""
    if 'code_submissions' not in st.session_state:
        st.session_state.code_submissions = []
    
    submission = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('user_data', {}).get('username', 'anonymous'),
        'language': code_data.get('language', ''),
        'code': code_data.get('code', ''),
        'exercise_id': code_data.get('exercise_id', ''),
        'result': code_data.get('result', ''),
        'ai_feedback': code_data.get('ai_feedback', {})
    }
    
    st.session_state.code_submissions.append(submission)

def save_course_evaluation(evaluation_data: Dict):
    """Save course evaluation to database"""
    if 'course_evaluations' not in st.session_state:
        st.session_state.course_evaluations = []
    
    evaluation = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('user_data', {}).get('username', 'anonymous'),
        'course_id': evaluation_data.get('course_id', ''),
        'rating': evaluation_data.get('rating', 0),
        'feedback': evaluation_data.get('feedback', ''),
        'difficulty_rating': evaluation_data.get('difficulty_rating', 0),
        'recommend': evaluation_data.get('recommend', False)
    }
    
    st.session_state.course_evaluations.append(evaluation)

def get_user_progress_data() -> Dict:
    """Get comprehensive user progress data"""
    username = st.session_state.get('user_data', {}).get('username', 'anonymous')
    
    # Filter activities for current user
    user_activities = [
        activity for activity in st.session_state.get('user_activities', [])
        if activity.get('user') == username
    ]
    
    # Filter quiz results for current user
    user_quiz_results = [
        result for result in st.session_state.get('quiz_results', [])
        if result.get('user') == username
    ]
    
    # Filter code submissions for current user
    user_code_submissions = [
        submission for submission in st.session_state.get('code_submissions', [])
        if submission.get('user') == username
    ]
    
    # Calculate statistics
    total_activities = len(user_activities)
    quiz_count = len(user_quiz_results)
    code_submissions_count = len(user_code_submissions)
    
    # Calculate average quiz score
    avg_quiz_score = 0
    if user_quiz_results:
        total_score = sum(result.get('score', 0) for result in user_quiz_results)
        total_possible = sum(result.get('total_questions', 0) for result in user_quiz_results)
        if total_possible > 0:
            avg_quiz_score = (total_score / total_possible) * 100
    
    # Count lessons completed (from activities)
    lesson_activities = [
        activity for activity in user_activities
        if activity.get('activity_type') == 'lesson_completed'
    ]
    
    return {
        'total_activities': total_activities,
        'lessons_completed': len(lesson_activities),
        'quiz_count': quiz_count,
        'code_submissions_count': code_submissions_count,
        'average_quiz_score': avg_quiz_score,
        'recent_activities': user_activities[-10:],  # Last 10 activities
        'quiz_results': user_quiz_results,
        'code_submissions': user_code_submissions
    }

def get_learning_analytics() -> Dict:
    """Get learning analytics for instructor dashboard"""
    all_activities = st.session_state.get('user_activities', [])
    all_quiz_results = st.session_state.get('quiz_results', [])
    all_code_submissions = st.session_state.get('code_submissions', [])
    
    # Create DataFrames for analysis
    activities_df = pd.DataFrame(all_activities)
    quiz_df = pd.DataFrame(all_quiz_results)
    code_df = pd.DataFrame(all_code_submissions)
    
    analytics = {
        'total_users': len(set(activities_df.get('user', []) if not activities_df.empty else [])),
        'total_activities': len(all_activities),
        'total_quizzes_taken': len(all_quiz_results),
        'total_code_submissions': len(all_code_submissions),
        'active_today': 0,  # Would need proper date filtering
        'popular_topics': {},
        'language_preferences': {},
        'average_scores': {}
    }
    
    if not quiz_df.empty:
        # Language preferences
        lang_counts = quiz_df['language'].value_counts().to_dict()
        analytics['language_preferences'] = lang_counts
        
        # Average scores by language
        avg_scores = quiz_df.groupby('language')['score'].mean().to_dict()
        analytics['average_scores'] = avg_scores
    
    return analytics

def export_user_data() -> str:
    """Export user data as JSON string"""
    user_data = get_user_progress_data()
    return json.dumps(user_data, indent=2, default=str)
