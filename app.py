import streamlit as st
import pandas as pd
from utils.auth import initialize_session, check_authentication
from utils.database import initialize_database

# Configure the page
st.set_page_config(
    page_title="PERL & Python Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and session
initialize_database()
initialize_session()

# Custom CSS for better styling (minimal, following guidelines)
st.markdown("""
<style>
    .stApp > header {
        background-color: transparent;
    }
    .main-header {
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎓 PERL & Python Learning Platform")
    st.markdown("### Comprehensive Learning with AI-Powered Support")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.warning("Please log in to access the learning platform.")
        
        # Login/Register tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_form()
        
        with tab2:
            register_form()
    else:
        # Welcome message
        st.success(f"Welcome back, {st.session_state.user_data['username']}!")
        
        # Main navigation info
        st.markdown("""
        ## 🚀 Getting Started
        
        Use the sidebar to navigate through different sections of the platform:
        
        - **🏠 Dashboard**: View your learning progress and recent activities
        - **📚 Courses**: Access PERL and Python course materials
        - **💻 Code Practice**: Interactive coding environment with AI assistance
        - **🤖 AI Chatbot**: Get instant help with your programming questions
        - **📝 Quizzes**: Test your knowledge with AI-generated questions
        - **📊 Progress**: Track your learning journey and achievements
        - **🔍 Search**: Find specific topics and lessons quickly
        - **⚙️ Settings**: Manage your profile and preferences
        """)
        
        # Platform features overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🧠 AI-Powered Learning</h4>
                <p>Get personalized help, code analysis, and instant feedback from our AI assistant.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>💻 Interactive Coding</h4>
                <p>Practice PERL and Python in our integrated development environment.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>📈 Progress Tracking</h4>
                <p>Monitor your learning progress with detailed analytics and assessments.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick stats
        if 'user_progress' in st.session_state:
            st.markdown("### 📊 Quick Stats")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Lessons Completed", st.session_state.user_progress.get('lessons_completed', 0))
            
            with col2:
                st.metric("Code Exercises", st.session_state.user_progress.get('exercises_completed', 0))
            
            with col3:
                st.metric("Quiz Score", f"{st.session_state.user_progress.get('average_quiz_score', 0):.1f}%")
            
            with col4:
                st.metric("Learning Streak", f"{st.session_state.user_progress.get('learning_streak', 0)} days")

def login_form():
    """Login form component"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me")
        
        if st.form_submit_button("Login", use_container_width=True):
            if username and password:
                # Simple authentication (in production, use proper password hashing)
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user_data = {
                        'username': username,
                        'role': 'student',  # Default role
                        'login_time': pd.Timestamp.now()
                    }
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")

def register_form():
    """Registration form component"""
    st.markdown("### 📝 Create New Account")
    
    with st.form("register_form"):
        username = st.text_input("Choose Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["student", "instructor"])
        
        if st.form_submit_button("Create Account", use_container_width=True):
            if username and email and password and confirm_password:
                if password == confirm_password:
                    if register_user(username, email, password, role):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists or registration failed")
                else:
                    st.error("Passwords do not match")
            else:
                st.warning("Please fill in all fields")

def authenticate_user(username, password):
    """Authentication function using PostgreSQL database"""
    from utils.auth import authenticate_user_db
    
    # Authenticate user against database
    return authenticate_user_db(username, password)

def register_user(username, email, password, role):
    """User registration function using PostgreSQL database"""
    from utils.auth import create_user
    
    # Register user in database
    return create_user(username, email, password, role)

if __name__ == "__main__":
    main()
