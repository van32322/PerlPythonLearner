import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import check_authentication, get_current_user, logout, update_user_progress, update_skill_level
from utils.database import log_user_activity, export_user_data

# Page configuration
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access settings.")
        return
    
    st.title("⚙️ Settings & Preferences")
    
    user = get_current_user()
    st.markdown(f"Welcome, **{user['username']}**! Manage your account and learning preferences below.")
    
    # Settings tabs
    tabs = st.tabs([
        "👤 Profile", 
        "🎯 Learning Preferences", 
        "📊 Privacy & Data", 
        "🔔 Notifications", 
        "🔐 Security",
        "📱 Account"
    ])
    
    with tabs[0]:
        show_profile_settings()
    
    with tabs[1]:
        show_learning_preferences()
    
    with tabs[2]:
        show_privacy_data_settings()
    
    with tabs[3]:
        show_notification_settings()
    
    with tabs[4]:
        show_security_settings()
    
    with tabs[5]:
        show_account_settings()
    
    # Log settings page visit
    log_user_activity('settings_page_visit', {'timestamp': datetime.now().isoformat()})

def show_profile_settings():
    """Display profile settings"""
    
    st.subheader("👤 Profile Information")
    
    user = get_current_user()
    users_db = st.session_state.get('users_db', {})
    user_data = users_db.get(user['username'], {})
    profile = user_data.get('profile', {})
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic info
            display_name = st.text_input(
                "Display Name:",
                value=user['username'],
                help="This name will be shown in the platform"
            )
            
            email = st.text_input(
                "Email Address:",
                value=user_data.get('email', ''),
                help="Used for notifications and account recovery"
            )
            
            bio = st.text_area(
                "Bio:",
                value=profile.get('bio', ''),
                help="Tell others about yourself and your programming journey"
            )
        
        with col2:
            # Learning info
            programming_experience = st.selectbox(
                "Programming Experience:",
                ["Complete Beginner", "Some Experience", "Intermediate", "Advanced", "Expert"],
                index=0
            )
            
            primary_language = st.selectbox(
                "Primary Programming Language Interest:",
                ["Python", "PERL", "Both Equally"],
                index=2
            )
            
            learning_goals = st.multiselect(
                "Learning Goals:",
                [
                    "Career Change", "Skill Enhancement", "Academic Requirements",
                    "Personal Projects", "Automation", "Data Analysis",
                    "Web Development", "System Administration"
                ],
                default=profile.get('learning_goals', [])
            )
        
        # Save button
        if st.form_submit_button("💾 Save Profile", use_container_width=True):
            # Update user profile
            if user['username'] in st.session_state.users_db:
                st.session_state.users_db[user['username']]['email'] = email
                st.session_state.users_db[user['username']]['profile'] = {
                    'bio': bio,
                    'learning_goals': learning_goals,
                    'programming_experience': programming_experience,
                    'primary_language': primary_language.lower(),
                    'display_name': display_name
                }
                
                st.success("✅ Profile updated successfully!")
                
                # Log activity
                log_user_activity('profile_updated', {
                    'display_name': display_name,
                    'primary_language': primary_language
                })
            else:
                st.error("Failed to update profile.")

def show_learning_preferences():
    """Display learning preferences"""
    
    st.subheader("🎯 Learning Preferences")
    
    # Get current preferences
    user_progress = st.session_state.get('user_progress', {})
    
    with st.form("learning_prefs_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Skill levels
            st.markdown("**Current Skill Levels:**")
            
            python_level = st.selectbox(
                "Python Skill Level:",
                ["beginner", "intermediate", "advanced"],
                index=["beginner", "intermediate", "advanced"].index(
                    user_progress.get('skill_levels', {}).get('python', 'beginner')
                )
            )
            
            perl_level = st.selectbox(
                "PERL Skill Level:",
                ["beginner", "intermediate", "advanced"],
                index=["beginner", "intermediate", "advanced"].index(
                    user_progress.get('skill_levels', {}).get('perl', 'beginner')
                )
            )
            
            # Learning pace
            learning_pace = st.selectbox(
                "Preferred Learning Pace:",
                ["Slow and Steady", "Moderate", "Fast Track", "Self-Paced"],
                index=2
            )
        
        with col2:
            # Preferences
            st.markdown("**Learning Preferences:**")
            
            difficulty_preference = st.selectbox(
                "Preferred Quiz Difficulty:",
                ["Easy", "Medium", "Hard", "Mixed"],
                index=3
            )
            
            code_style = st.selectbox(
                "Code Editor Theme:",
                ["Light", "Dark", "Auto"],
                index=1
            )
            
            ai_assistance_level = st.selectbox(
                "AI Assistance Level:",
                ["Minimal", "Moderate", "Maximum", "On-Demand"],
                index=2
            )
            
            # Notifications
            daily_reminders = st.checkbox("Daily Learning Reminders", value=True)
            achievement_notifications = st.checkbox("Achievement Notifications", value=True)
            progress_reports = st.checkbox("Weekly Progress Reports", value=True)
        
        if st.form_submit_button("💾 Save Preferences", use_container_width=True):
            # Update skill levels
            update_skill_level('python', python_level)
            update_skill_level('perl', perl_level)
            
            # Store other preferences
            if 'learning_preferences' not in st.session_state:
                st.session_state.learning_preferences = {}
            
            st.session_state.learning_preferences.update({
                'learning_pace': learning_pace,
                'difficulty_preference': difficulty_preference,
                'code_style': code_style,
                'ai_assistance_level': ai_assistance_level,
                'daily_reminders': daily_reminders,
                'achievement_notifications': achievement_notifications,
                'progress_reports': progress_reports
            })
            
            st.success("✅ Learning preferences updated!")
            
            # Log activity
            log_user_activity('preferences_updated', {
                'python_level': python_level,
                'perl_level': perl_level,
                'learning_pace': learning_pace
            })

def show_privacy_data_settings():
    """Display privacy and data settings"""
    
    st.subheader("📊 Privacy & Data Management")
    
    # Data overview
    st.markdown("**Your Data Overview:**")
    
    progress_data = st.session_state.get('user_progress', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Lessons Completed", progress_data.get('lessons_completed', 0))
    
    with col2:
        quiz_count = len([r for r in st.session_state.get('quiz_results', []) 
                         if r.get('user') == get_current_user()['username']])
        st.metric("Quizzes Taken", quiz_count)
    
    with col3:
        code_count = len([s for s in st.session_state.get('code_submissions', []) 
                         if s.get('user') == get_current_user()['username']])
        st.metric("Code Submissions", code_count)
    
    with col4:
        activity_count = len([a for a in st.session_state.get('user_activities', []) 
                             if a.get('user') == get_current_user()['username']])
        st.metric("Total Activities", activity_count)
    
    st.divider()
    
    # Privacy settings
    st.markdown("**Privacy Settings:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Data sharing preferences
        st.markdown("**Data Sharing:**")
        
        share_progress = st.checkbox(
            "Share progress with instructors",
            value=True,
            help="Allow instructors to see your learning progress"
        )
        
        share_analytics = st.checkbox(
            "Contribute to anonymous analytics",
            value=True,
            help="Help improve the platform with anonymous usage data"
        )
        
        public_profile = st.checkbox(
            "Make profile visible to other students",
            value=False,
            help="Other students can see your basic profile information"
        )
    
    with col2:
        # Data retention
        st.markdown("**Data Management:**")
        
        if st.button("📥 Export My Data", use_container_width=True):
            try:
                user_data_json = export_user_data()
                st.download_button(
                    label="💾 Download Data Export",
                    data=user_data_json,
                    file_name=f"my_learning_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                st.success("✅ Data export ready for download!")
            except Exception as e:
                st.error(f"Failed to export data: {str(e)}")
        
        if st.button("🗑️ Clear Learning History", use_container_width=True):
            st.warning("⚠️ This will permanently delete your learning history!")
            
            confirm = st.checkbox("I understand this action cannot be undone")
            
            if confirm and st.button("Confirm Deletion", type="primary"):
                clear_user_data()
                st.success("✅ Learning history cleared!")
                st.rerun()

def show_notification_settings():
    """Display notification settings"""
    
    st.subheader("🔔 Notification Preferences")
    
    with st.form("notification_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Learning Reminders:**")
            
            daily_reminder = st.checkbox("Daily learning reminder", value=True)
            reminder_time = st.time_input("Reminder time:", value=pd.to_datetime("19:00").time())
            
            weekly_summary = st.checkbox("Weekly progress summary", value=True)
            
            st.markdown("**Achievement Notifications:**")
            
            badge_earned = st.checkbox("New badges and achievements", value=True)
            milestone_reached = st.checkbox("Learning milestones", value=True)
            streak_notifications = st.checkbox("Learning streak updates", value=True)
        
        with col2:
            st.markdown("**Course Notifications:**")
            
            new_content = st.checkbox("New course content available", value=True)
            assignment_due = st.checkbox("Assignment due dates", value=True)
            
            st.markdown("**Social Notifications:**")
            
            instructor_feedback = st.checkbox("Instructor feedback", value=True)
            peer_interactions = st.checkbox("Peer interactions", value=False)
            
            st.markdown("**System Notifications:**")
            
            maintenance_alerts = st.checkbox("Maintenance and updates", value=True)
            security_alerts = st.checkbox("Security notifications", value=True)
        
        if st.form_submit_button("💾 Save Notification Settings", use_container_width=True):
            # Store notification preferences
            notification_prefs = {
                'daily_reminder': daily_reminder,
                'reminder_time': str(reminder_time),
                'weekly_summary': weekly_summary,
                'badge_earned': badge_earned,
                'milestone_reached': milestone_reached,
                'streak_notifications': streak_notifications,
                'new_content': new_content,
                'assignment_due': assignment_due,
                'instructor_feedback': instructor_feedback,
                'peer_interactions': peer_interactions,
                'maintenance_alerts': maintenance_alerts,
                'security_alerts': security_alerts
            }
            
            st.session_state.notification_preferences = notification_prefs
            st.success("✅ Notification preferences updated!")
            
            # Log activity
            log_user_activity('notification_prefs_updated', notification_prefs)

def show_security_settings():
    """Display security settings"""
    
    st.subheader("🔐 Security Settings")
    
    # Password change
    st.markdown("**Change Password:**")
    
    with st.form("password_form"):
        current_password = st.text_input("Current Password:", type="password")
        new_password = st.text_input("New Password:", type="password")
        confirm_password = st.text_input("Confirm New Password:", type="password")
        
        if st.form_submit_button("🔐 Change Password"):
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill in all password fields.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                # Verify current password (simplified)
                user = get_current_user()
                users_db = st.session_state.get('users_db', {})
                
                if (user['username'] in users_db and 
                    users_db[user['username']].get('password') == current_password):
                    
                    # Update password
                    users_db[user['username']]['password'] = new_password
                    st.success("✅ Password changed successfully!")
                    
                    # Log activity
                    log_user_activity('password_changed', {'timestamp': datetime.now().isoformat()})
                else:
                    st.error("Current password is incorrect.")
    
    st.divider()
    
    # Security options
    st.markdown("**Security Options:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        two_factor_auth = st.checkbox(
            "Enable Two-Factor Authentication",
            value=False,
            help="Add an extra layer of security to your account"
        )
        
        if two_factor_auth:
            st.info("📱 Two-factor authentication setup would be implemented here")
    
    with col2:
        login_notifications = st.checkbox(
            "Login notifications",
            value=True,
            help="Get notified of new login attempts"
        )
        
        session_timeout = st.selectbox(
            "Session timeout:",
            ["1 hour", "4 hours", "8 hours", "24 hours"],
            index=2
        )
    
    # Active sessions
    st.markdown("**Active Sessions:**")
    
    # Mock session data
    sessions = [
        {"device": "Current Browser", "location": "Local", "last_active": "Now", "current": True},
        {"device": "Mobile Browser", "location": "Mobile", "last_active": "2 hours ago", "current": False}
    ]
    
    for session in sessions:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            device_icon = "🖥️" if "Browser" in session["device"] else "📱"
            current_badge = " (Current)" if session["current"] else ""
            st.write(f"{device_icon} {session['device']}{current_badge}")
        
        with col2:
            st.write(session["location"])
        
        with col3:
            st.write(session["last_active"])
        
        with col4:
            if not session["current"]:
                if st.button("🚫", key=f"revoke_{session['device']}", help="Revoke session"):
                    st.success(f"Session revoked for {session['device']}")

def show_account_settings():
    """Display account settings"""
    
    st.subheader("📱 Account Management")
    
    user = get_current_user()
    users_db = st.session_state.get('users_db', {})
    user_data = users_db.get(user['username'], {})
    
    # Account info
    st.markdown("**Account Information:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Username:** {user['username']}")
        st.info(f"**Email:** {user_data.get('email', 'Not set')}")
        st.info(f"**Role:** {user.get('role', 'student').title()}")
    
    with col2:
        created_at = user_data.get('created_at')
        if created_at:
            if hasattr(created_at, 'strftime'):
                created_date = created_at.strftime('%Y-%m-%d')
            else:
                created_date = str(created_at)[:10]
        else:
            created_date = "Unknown"
        
        st.info(f"**Member Since:** {created_date}")
        st.info(f"**Last Login:** {user.get('login_time', 'Current session')}")
    
    st.divider()
    
    # Account actions
    st.markdown("**Account Actions:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset Learning Progress", use_container_width=True):
            st.warning("⚠️ This will reset all your learning progress!")
            
            if st.checkbox("I want to reset my progress"):
                if st.button("Confirm Reset", type="primary"):
                    reset_learning_progress()
                    st.success("✅ Learning progress has been reset!")
                    st.rerun()
    
    with col2:
        if st.button("📥 Download Account Data", use_container_width=True):
            try:
                account_data = {
                    'username': user['username'],
                    'email': user_data.get('email', ''),
                    'role': user.get('role', 'student'),
                    'created_at': str(user_data.get('created_at', '')),
                    'profile': user_data.get('profile', {}),
                    'progress': st.session_state.get('user_progress', {}),
                    'preferences': st.session_state.get('learning_preferences', {})
                }
                
                import json
                account_json = json.dumps(account_data, indent=2, default=str)
                
                st.download_button(
                    label="💾 Download Account Data",
                    data=account_json,
                    file_name=f"account_data_{user['username']}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Failed to prepare account data: {str(e)}")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            # Log logout activity
            log_user_activity('user_logout', {'timestamp': datetime.now().isoformat()})
            
            # Logout user
            logout()
    
    st.divider()
    
    # Danger zone
    with st.expander("🚨 Danger Zone", expanded=False):
        st.error("**Delete Account**")
        st.markdown("Permanently delete your account and all associated data. This action cannot be undone.")
        
        delete_confirmation = st.text_input(
            "Type 'DELETE' to confirm account deletion:",
            placeholder="DELETE"
        )
        
        if delete_confirmation == "DELETE":
            if st.button("🗑️ Delete My Account", type="primary"):
                # Log account deletion
                log_user_activity('account_deleted', {'timestamp': datetime.now().isoformat()})
                
                # Delete user data
                if user['username'] in st.session_state.users_db:
                    del st.session_state.users_db[user['username']]
                
                # Clear user progress
                clear_user_data()
                
                # Logout
                st.session_state.authenticated = False
                st.session_state.user_data = {}
                
                st.success("Account deleted successfully. Thank you for using our platform!")
                st.rerun()

def clear_user_data():
    """Clear all user-specific data"""
    
    user = get_current_user()
    username = user['username']
    
    # Clear user activities
    if 'user_activities' in st.session_state:
        st.session_state.user_activities = [
            activity for activity in st.session_state.user_activities
            if activity.get('user') != username
        ]
    
    # Clear quiz results
    if 'quiz_results' in st.session_state:
        st.session_state.quiz_results = [
            result for result in st.session_state.quiz_results
            if result.get('user') != username
        ]
    
    # Clear code submissions
    if 'code_submissions' in st.session_state:
        st.session_state.code_submissions = [
            submission for submission in st.session_state.code_submissions
            if submission.get('user') != username
        ]
    
    # Reset user progress
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

def reset_learning_progress():
    """Reset only learning progress, keep account data"""
    
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

if __name__ == "__main__":
    main()
