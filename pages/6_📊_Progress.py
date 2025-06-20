import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.auth import check_authentication, get_current_user, is_instructor
from utils.database import get_user_progress_data, get_learning_analytics
from utils.ai_services import ai_assistant

# Page configuration
st.set_page_config(page_title="Progress Tracking", page_icon="📊", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to view your progress.")
        return
    
    st.title("📊 Learning Progress & Analytics")
    
    if is_instructor():
        show_instructor_analytics()
    else:
        show_student_progress()

def show_student_progress():
    """Display student progress tracking"""
    
    user = get_current_user()
    st.subheader(f"🎯 {user['username']}'s Learning Journey")
    
    # Get progress data
    progress_data = get_user_progress_data()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Activities",
            progress_data['total_activities'],
            help="Total learning activities including lessons, quizzes, and coding exercises"
        )
    
    with col2:
        st.metric(
            "Lessons Completed",
            progress_data['lessons_completed'],
            help="Number of course lessons you've completed"
        )
    
    with col3:
        st.metric(
            "Quiz Average",
            f"{progress_data['average_quiz_score']:.1f}%",
            help="Your average score across all quizzes taken"
        )
    
    with col4:
        # Calculate learning streak (simplified)
        learning_streak = calculate_learning_streak(progress_data['recent_activities'])
        st.metric(
            "Learning Streak",
            f"{learning_streak} days",
            help="Consecutive days of learning activity"
        )
    
    # Progress charts
    col1, col2 = st.columns(2)
    
    with col1:
        show_activity_timeline(progress_data)
    
    with col2:
        show_quiz_performance_chart(progress_data)
    
    # Skill assessment
    show_skill_assessment()
    
    # Learning goals
    show_learning_goals()
    
    # Detailed progress breakdown
    show_detailed_progress(progress_data)

def show_instructor_analytics():
    """Display instructor analytics dashboard"""
    
    st.subheader("👨‍🏫 Class Analytics Dashboard")
    
    # Get analytics data
    analytics = get_learning_analytics()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", analytics['total_users'])
    
    with col2:
        st.metric("Total Activities", analytics['total_activities'])
    
    with col3:
        st.metric("Quizzes Completed", analytics['total_quizzes_taken'])
    
    with col4:
        st.metric("Code Submissions", analytics['total_code_submissions'])
    
    # Analytics charts
    col1, col2 = st.columns(2)
    
    with col1:
        show_language_preferences_chart(analytics)
    
    with col2:
        show_class_performance_chart(analytics)
    
    # Student activity heatmap
    show_activity_heatmap()
    
    # Course effectiveness analysis
    show_course_effectiveness()

def show_activity_timeline(progress_data):
    """Show activity timeline chart"""
    
    st.subheader("📈 Activity Timeline")
    
    if not progress_data['recent_activities']:
        st.info("No activity data available yet. Start learning to see your progress!")
        return
    
    # Process activity data
    activities_df = pd.DataFrame(progress_data['recent_activities'])
    activities_df['timestamp'] = pd.to_datetime(activities_df['timestamp'])
    activities_df['date'] = activities_df['timestamp'].dt.date
    activities_df['hour'] = activities_df['timestamp'].dt.hour
    
    # Daily activity count
    daily_activities = activities_df.groupby('date').size().reset_index(name='activity_count')
    
    if not daily_activities.empty:
        fig = px.line(
            daily_activities,
            x='date',
            y='activity_count',
            title='Daily Learning Activities',
            labels={'activity_count': 'Activities', 'date': 'Date'}
        )
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
    
    # Activity type breakdown
    if 'activity_type' in activities_df.columns:
        activity_types = activities_df['activity_type'].value_counts()
        
        fig_pie = px.pie(
            values=activity_types.values,
            names=activity_types.index,
            title='Activity Types Distribution'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def show_quiz_performance_chart(progress_data):
    """Show quiz performance over time"""
    
    st.subheader("🎯 Quiz Performance")
    
    if not progress_data['quiz_results']:
        st.info("Take some quizzes to see your performance trends!")
        return
    
    # Process quiz data
    quiz_df = pd.DataFrame(progress_data['quiz_results'])
    quiz_df['timestamp'] = pd.to_datetime(quiz_df['timestamp'])
    quiz_df['score_percentage'] = (quiz_df['score'] / quiz_df['total_questions']) * 100
    
    # Performance over time
    fig = px.line(
        quiz_df,
        x='timestamp',
        y='score_percentage',
        color='language',
        title='Quiz Scores Over Time',
        labels={'score_percentage': 'Score %', 'timestamp': 'Date'}
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Target: 70%")
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance by topic
    if 'quiz_topic' in quiz_df.columns:
        topic_performance = quiz_df.groupby('quiz_topic')['score_percentage'].mean().reset_index()
        
        fig_bar = px.bar(
            topic_performance,
            x='quiz_topic',
            y='score_percentage',
            title='Average Score by Topic',
            labels={'score_percentage': 'Average Score %', 'quiz_topic': 'Topic'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def show_skill_assessment():
    """Show skill level assessment"""
    
    st.subheader("🎯 Skill Assessment")
    
    # Get current skill levels from session state
    skill_levels = st.session_state.get('user_progress', {}).get('skill_levels', {
        'python': 'beginner',
        'perl': 'beginner'
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Python Programming**")
        python_level = skill_levels.get('python', 'beginner')
        progress_value = {'beginner': 33, 'intermediate': 66, 'advanced': 100}.get(python_level, 33)
        st.progress(progress_value / 100)
        st.write(f"Current Level: {python_level.title()}")
    
    with col2:
        st.markdown("**PERL Programming**")
        perl_level = skill_levels.get('perl', 'beginner')
        progress_value = {'beginner': 33, 'intermediate': 66, 'advanced': 100}.get(perl_level, 33)
        st.progress(progress_value / 100)
        st.write(f"Current Level: {perl_level.title()}")
    
    # Skill assessment quiz
    if st.button("📝 Take Skill Assessment"):
        st.info("Skill assessment feature would launch a comprehensive quiz to evaluate your current skill level.")

def show_learning_goals():
    """Show and manage learning goals"""
    
    st.subheader("🎯 Learning Goals")
    
    # Initialize goals if not exists
    if 'learning_goals' not in st.session_state:
        st.session_state.learning_goals = [
            {"goal": "Complete Python Basics module", "completed": False, "target_date": "2024-12-31"},
            {"goal": "Score 80%+ on PERL quiz", "completed": False, "target_date": "2024-12-31"},
            {"goal": "Submit 10 code exercises", "completed": False, "target_date": "2024-12-31"}
        ]
    
    # Display goals
    for i, goal in enumerate(st.session_state.learning_goals):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if goal['completed']:
                st.success(f"✅ {goal['goal']}")
            else:
                st.write(f"🎯 {goal['goal']}")
        
        with col2:
            st.write(f"Target: {goal['target_date']}")
        
        with col3:
            if not goal['completed']:
                if st.button("Mark Done", key=f"goal_{i}"):
                    st.session_state.learning_goals[i]['completed'] = True
                    st.rerun()
    
    # Add new goal
    with st.expander("➕ Add New Goal"):
        new_goal = st.text_input("Goal description:")
        target_date = st.date_input("Target date:")
        
        if st.button("Add Goal"):
            if new_goal:
                st.session_state.learning_goals.append({
                    "goal": new_goal,
                    "completed": False,
                    "target_date": str(target_date)
                })
                st.success("Goal added!")
                st.rerun()

def show_detailed_progress(progress_data):
    """Show detailed progress breakdown"""
    
    st.subheader("📋 Detailed Progress Report")
    
    # Create tabs for different aspects
    tabs = st.tabs(["📚 Course Progress", "💻 Coding Activity", "📝 Quiz History", "🏆 Achievements"])
    
    with tabs[0]:
        show_course_progress()
    
    with tabs[1]:
        show_coding_activity(progress_data)
    
    with tabs[2]:
        show_quiz_history(progress_data)
    
    with tabs[3]:
        show_achievements()

def show_course_progress():
    """Show detailed course progress"""
    
    # Mock course progress data
    course_progress = {
        'python': {
            'modules_completed': 2,
            'total_modules': 5,
            'lessons_completed': 8,
            'total_lessons': 25,
            'last_activity': '2024-06-19'
        },
        'perl': {
            'modules_completed': 1,
            'total_modules': 4,
            'lessons_completed': 3,
            'total_lessons': 20,
            'last_activity': '2024-06-18'
        }
    }
    
    for course, progress in course_progress.items():
        st.markdown(f"**{course.upper()} Course Progress**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            module_progress = progress['modules_completed'] / progress['total_modules']
            st.metric("Modules", f"{progress['modules_completed']}/{progress['total_modules']}")
            st.progress(module_progress)
        
        with col2:
            lesson_progress = progress['lessons_completed'] / progress['total_lessons']
            st.metric("Lessons", f"{progress['lessons_completed']}/{progress['total_lessons']}")
            st.progress(lesson_progress)
        
        with col3:
            st.metric("Last Activity", progress['last_activity'])
        
        st.divider()

def show_coding_activity(progress_data):
    """Show coding activity details"""
    
    if not progress_data['code_submissions']:
        st.info("No coding activity yet. Start practicing to see your progress!")
        return
    
    # Process coding submissions
    code_df = pd.DataFrame(progress_data['code_submissions'])
    
    # Language distribution
    if 'language' in code_df.columns:
        lang_counts = code_df['language'].value_counts()
        
        fig = px.pie(
            values=lang_counts.values,
            names=lang_counts.index,
            title='Code Submissions by Language'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent submissions
    st.markdown("**Recent Code Submissions:**")
    recent_submissions = code_df.tail(5)
    
    for _, submission in recent_submissions.iterrows():
        timestamp = pd.to_datetime(submission['timestamp']).strftime('%Y-%m-%d %H:%M')
        st.markdown(f"• {submission['language'].title()} - {timestamp}")

def show_quiz_history(progress_data):
    """Show detailed quiz history"""
    
    if not progress_data['quiz_results']:
        st.info("No quiz history yet. Take some quizzes to see your progress!")
        return
    
    quiz_df = pd.DataFrame(progress_data['quiz_results'])
    quiz_df['score_percentage'] = (quiz_df['score'] / quiz_df['total_questions']) * 100
    quiz_df['timestamp'] = pd.to_datetime(quiz_df['timestamp'])
    
    # Display as table
    display_df = quiz_df[['timestamp', 'quiz_topic', 'language', 'score', 'total_questions', 'score_percentage']].copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    display_df.columns = ['Date', 'Topic', 'Language', 'Score', 'Total', 'Percentage']
    
    st.dataframe(display_df, use_container_width=True)

def show_achievements():
    """Show user achievements and badges"""
    
    st.markdown("**🏆 Your Achievements**")
    
    # Calculate achievements based on progress
    achievements = []
    
    # Get user progress
    progress_data = get_user_progress_data()
    
    if progress_data['lessons_completed'] >= 1:
        achievements.append("📚 First Lesson Completed")
    
    if progress_data['lessons_completed'] >= 5:
        achievements.append("🎓 Learning Enthusiast")
    
    if progress_data['quiz_count'] >= 1:
        achievements.append("📝 Quiz Taker")
    
    if progress_data['average_quiz_score'] >= 80:
        achievements.append("🌟 High Achiever")
    
    if progress_data['code_submissions_count'] >= 5:
        achievements.append("💻 Code Warrior")
    
    if not achievements:
        st.info("Start learning to unlock achievements!")
    else:
        for achievement in achievements:
            st.success(achievement)

def show_language_preferences_chart(analytics):
    """Show class language preferences"""
    
    st.subheader("📊 Class Language Preferences")
    
    if analytics['language_preferences']:
        lang_data = pd.DataFrame(
            list(analytics['language_preferences'].items()),
            columns=['Language', 'Students']
        )
        
        fig = px.bar(
            lang_data,
            x='Language',
            y='Students',
            title='Students by Programming Language'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No language preference data available yet.")

def show_class_performance_chart(analytics):
    """Show class performance metrics"""
    
    st.subheader("🎯 Class Performance")
    
    if analytics['average_scores']:
        scores_data = pd.DataFrame(
            list(analytics['average_scores'].items()),
            columns=['Language', 'Average Score']
        )
        
        fig = px.bar(
            scores_data,
            x='Language',
            y='Average Score',
            title='Average Quiz Scores by Language'
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Target: 70%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No performance data available yet.")

def show_activity_heatmap():
    """Show student activity heatmap"""
    
    st.subheader("🔥 Activity Heatmap")
    
    # Mock heatmap data
    if st.session_state.get('user_activities'):
        activities_df = pd.DataFrame(st.session_state['user_activities'])
        activities_df['timestamp'] = pd.to_datetime(activities_df['timestamp'])
        activities_df['date'] = activities_df['timestamp'].dt.date
        activities_df['hour'] = activities_df['timestamp'].dt.hour
        
        # Create heatmap data
        heatmap_data = activities_df.groupby(['date', 'hour']).size().reset_index(name='activity_count')
        
        if not heatmap_data.empty:
            # Create pivot table for heatmap
            pivot_data = heatmap_data.pivot(index='hour', columns='date', values='activity_count').fillna(0)
            
            fig = px.imshow(
                pivot_data,
                title='Student Activity Heatmap (Hour vs Date)',
                labels={'x': 'Date', 'y': 'Hour of Day', 'color': 'Activities'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity data available for heatmap.")

def show_course_effectiveness():
    """Show course effectiveness metrics"""
    
    st.subheader("📈 Course Effectiveness")
    
    # Mock effectiveness data
    effectiveness_data = {
        'Python Basics': {'completion_rate': 85, 'avg_score': 78, 'student_rating': 4.2},
        'PERL Fundamentals': {'completion_rate': 72, 'avg_score': 74, 'student_rating': 3.9},
        'Advanced Python': {'completion_rate': 60, 'avg_score': 82, 'student_rating': 4.5}
    }
    
    for course, metrics in effectiveness_data.items():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{course}**")
        
        with col2:
            st.metric("Completion Rate", f"{metrics['completion_rate']}%")
        
        with col3:
            st.metric("Avg Score", f"{metrics['avg_score']}%")
        
        with col4:
            st.metric("Rating", f"{metrics['student_rating']}/5.0")

def calculate_learning_streak(activities):
    """Calculate learning streak in days"""
    
    if not activities:
        return 0
    
    # Get unique dates with activity
    activity_dates = set()
    for activity in activities:
        activity_date = pd.to_datetime(activity['timestamp']).date()
        activity_dates.add(activity_date)
    
    if not activity_dates:
        return 0
    
    # Sort dates
    sorted_dates = sorted(activity_dates, reverse=True)
    
    # Calculate streak
    streak = 1
    current_date = sorted_dates[0]
    
    for i in range(1, len(sorted_dates)):
        previous_date = sorted_dates[i]
        if (current_date - previous_date).days == 1:
            streak += 1
            current_date = previous_date
        else:
            break
    
    return streak

if __name__ == "__main__":
    main()
