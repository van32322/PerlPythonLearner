import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.auth import check_authentication, get_current_user, is_instructor
from utils.database import get_user_progress_data, get_learning_analytics, log_user_activity
from utils.ai_services import ai_assistant

# Page configuration
st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access the dashboard.")
        return
    
    user = get_current_user()
    st.title(f"🏠 Welcome back, {user['username']}!")
    
    if is_instructor():
        show_instructor_dashboard()
    else:
        show_student_dashboard()

def show_student_dashboard():
    """Show student dashboard with progress and recommendations"""
    
    # Log dashboard visit
    log_user_activity('dashboard_visit', {'page': 'student_dashboard'})
    
    # Get user progress data
    progress_data = get_user_progress_data()
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Lessons Completed", 
            progress_data['lessons_completed'],
            delta=None
        )
    
    with col2:
        st.metric(
            "Quizzes Taken", 
            progress_data['quiz_count'],
            delta=None
        )
    
    with col3:
        st.metric(
            "Code Submissions", 
            progress_data['code_submissions_count'],
            delta=None
        )
    
    with col4:
        st.metric(
            "Average Score", 
            f"{progress_data['average_quiz_score']:.1f}%",
            delta=None
        )
    
    # Create two columns for main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Learning Progress Chart
        st.subheader("📈 Learning Progress")
        
        if progress_data['recent_activities']:
            # Create activity timeline
            activities_df = pd.DataFrame(progress_data['recent_activities'])
            activities_df['timestamp'] = pd.to_datetime(activities_df['timestamp'])
            activities_df['date'] = activities_df['timestamp'].dt.date
            
            # Count activities by date
            daily_activities = activities_df.groupby('date').size().reset_index(name='count')
            
            fig = px.line(
                daily_activities, 
                x='date', 
                y='count',
                title='Daily Learning Activities',
                labels={'count': 'Activities', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start learning to see your progress here!")
        
        # Quiz Performance
        if progress_data['quiz_results']:
            st.subheader("🎯 Quiz Performance")
            
            quiz_df = pd.DataFrame(progress_data['quiz_results'])
            quiz_df['score_percentage'] = (quiz_df['score'] / quiz_df['total_questions']) * 100
            
            fig = px.bar(
                quiz_df,
                x='quiz_topic',
                y='score_percentage',
                color='language',
                title='Quiz Scores by Topic',
                labels={'score_percentage': 'Score %', 'quiz_topic': 'Topic'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # AI Recommendations
        st.subheader("🤖 AI Recommendations")
        
        try:
            recommendations = ai_assistant.get_learning_recommendations(
                st.session_state.get('user_progress', {}),
                current_topic=""
            )
            
            for i, rec in enumerate(recommendations[:5], 1):
                st.markdown(f"**{i}.** {rec}")
        except Exception as e:
            st.warning("Unable to load AI recommendations at this time.")
        
        # Recent Activities
        st.subheader("📝 Recent Activities")
        
        if progress_data['recent_activities']:
            for activity in progress_data['recent_activities'][-5:]:
                activity_time = pd.to_datetime(activity['timestamp']).strftime('%H:%M')
                activity_type = activity['activity_type'].replace('_', ' ').title()
                st.text(f"{activity_time} - {activity_type}")
        else:
            st.info("No recent activities")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("Continue Learning", use_container_width=True):
            st.switch_page("pages/2_📚_Courses.py")
        
        if st.button("Practice Coding", use_container_width=True):
            st.switch_page("pages/3_💻_Code_Practice.py")
        
        if st.button("Take Quiz", use_container_width=True):
            st.switch_page("pages/5_📝_Quizzes.py")
        
        if st.button("Ask AI Assistant", use_container_width=True):
            st.switch_page("pages/4_🤖_AI_Chatbot.py")

def show_instructor_dashboard():
    """Show instructor dashboard with analytics and course management"""
    
    st.subheader("👨‍🏫 Instructor Dashboard")
    
    # Log dashboard visit
    log_user_activity('dashboard_visit', {'page': 'instructor_dashboard'})
    
    # Get learning analytics
    analytics = get_learning_analytics()
    
    # Analytics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", analytics['total_users'])
    
    with col2:
        st.metric("Total Activities", analytics['total_activities'])
    
    with col3:
        st.metric("Quizzes Taken", analytics['total_quizzes_taken'])
    
    with col4:
        st.metric("Code Submissions", analytics['total_code_submissions'])
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Language Preferences
        if analytics['language_preferences']:
            st.subheader("📊 Language Preferences")
            
            lang_data = pd.DataFrame(
                list(analytics['language_preferences'].items()),
                columns=['Language', 'Count']
            )
            
            fig = px.pie(
                lang_data,
                values='Count',
                names='Language',
                title='Student Language Preferences'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average Scores
        if analytics['average_scores']:
            st.subheader("🎯 Average Scores by Language")
            
            scores_data = pd.DataFrame(
                list(analytics['average_scores'].items()),
                columns=['Language', 'Average Score']
            )
            
            fig = px.bar(
                scores_data,
                x='Language',
                y='Average Score',
                title='Average Quiz Scores'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Course Management Section
    st.subheader("📚 Course Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Manage Python Course", use_container_width=True):
            st.info("Course management features would be implemented here")
    
    with col2:
        if st.button("Manage PERL Course", use_container_width=True):
            st.info("Course management features would be implemented here")
    
    with col3:
        if st.button("View All Submissions", use_container_width=True):
            st.info("Submission review features would be implemented here")
    
    # Recent Student Activities
    st.subheader("📈 Recent Student Activities")
    
    if st.session_state.get('user_activities'):
        recent_activities = st.session_state['user_activities'][-10:]
        
        activities_df = pd.DataFrame(recent_activities)
        if not activities_df.empty:
            activities_df['timestamp'] = pd.to_datetime(activities_df['timestamp'])
            activities_df = activities_df.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                activities_df[['timestamp', 'user', 'activity_type']],
                use_container_width=True
            )
    else:
        st.info("No recent activities to display")

if __name__ == "__main__":
    main()
