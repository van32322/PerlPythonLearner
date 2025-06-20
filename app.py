import streamlit as st
import pandas as pd
from utils.auth import initialize_session, check_authentication
from utils.database import initialize_database

# Configure the page with Mitsuri theme
st.set_page_config(
    page_title="🌸 Mitsuri's Coding Dojo - PERL & Python Platform",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_mitsuri_theme():
    """Apply Mitsuri background image theme"""
    # Convert image to base64 for embedding
    import base64
    
    try:
        with open("mitsuri.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.1);
            z-index: -1;
        }}
        
        .main .block-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        h1, h2, h3 {{
            color: #d63384 !important;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
        }}
        
        .stButton > button {{
            background: linear-gradient(45deg, #ff6b9d, #ff8fab);
            color: white;
            border: none;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(45deg, #ff8fab, #ffb3d9);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
        }}
        
        .feature-card {{
            background: rgba(255, 255, 255, 0.9);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 4px solid #ff6b9d;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
        }}
        
        .feature-card h4 {{
            color: #d63384;
            margin-bottom: 0.5rem;
        }}
        
        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 182, 193, 0.3);
        }}
        
        .stTextInput input, .stTextArea textarea {{
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid rgba(255, 182, 193, 0.3);
            border-radius: 10px;
        }}
        
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
        }}
        </style>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        # Fallback to gradient background if image fails to load
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #ffb3d9, #ff80cc, #ffccf2);
            background-attachment: fixed;
        }
        
        .main .block-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(255, 182, 193, 0.3);
        }
        
        h1, h2, h3 {
            color: #d63384 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialize database and session
initialize_database()
initialize_session()

# Apply Mitsuri theme
apply_mitsuri_theme()

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
    # Mitsuri-themed Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #d63384; font-size: 3rem; text-shadow: 2px 2px 4px rgba(255, 182, 193, 0.5);'>
            🌸 PERL & Python Learning Platform 🌸
        </h1>
        <h3 style='color: #ff6b9d; font-style: italic; text-shadow: 1px 1px 2px rgba(255, 182, 193, 0.3);'>
            Master programming with the strength and passion of Mitsuri Kanroji!
        </h3>
        <p style='color: #8b0049; font-size: 1.2rem; margin-top: 1rem;'>
            🗡️ Comprehensive Learning • 🤖 AI-Powered Support • 💪 Practice with Determination
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Try database authentication first
    user_data = authenticate_user_db(username, password)
    if user_data:
        return user_data
    
    # Fallback to session-based authentication
    users_db = st.session_state.get('users_db', {})
    user = users_db.get(username)
    if user and user.get('password') == password:
        return user
    return None

def register_user(username, email, password, role):
    """User registration function using PostgreSQL database"""
    from utils.auth import create_user
    
    # Try database registration first
    if create_user(username, email, password, role):
        return True
    
    # Fallback to session-based registration
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {}
    
    if username in st.session_state.users_db:
        return False
    
    st.session_state.users_db[username] = {
        'email': email,
        'password': password,
        'role': role,
        'created_at': pd.Timestamp.now(),
        'profile': {
            'bio': '',
            'learning_goals': [],
            'preferred_language': 'python'
        }
    }
    return True

if __name__ == "__main__":
    main()
