import streamlit as st
import markdown
from utils.auth import check_authentication, get_current_user
from utils.course_data import course_manager
from utils.database import log_user_activity, save_code_submission
from utils.ai_services import ai_assistant
from utils.code_executor import code_executor

# Page configuration
st.set_page_config(page_title="Courses", page_icon="📚", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access courses.")
        return
    
    st.title("📚 Programming Courses")
    
    # Course selection
    course_tabs = st.tabs(["🐍 Python Course", "🔤 PERL Course"])
    
    with course_tabs[0]:
        show_course_content('python')
    
    with course_tabs[1]:
        show_course_content('perl')

def show_course_content(course_id):
    """Display course content with navigation"""
    
    course = course_manager.get_course(course_id)
    
    if not course:
        st.error(f"Course {course_id} not found")
        return
    
    # Course header
    st.header(course['title'])
    st.markdown(f"**Description:** {course['description']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Difficulty", course['difficulty'])
    with col2:
        st.metric("Estimated Hours", course['estimated_hours'])
    with col3:
        st.metric("Modules", len(course['modules']))
    
    st.divider()
    
    # Module and lesson selection
    modules = course.get('modules', [])
    
    if not modules:
        st.warning("No modules available for this course yet.")
        return
    
    # Sidebar for navigation
    with st.sidebar:
        st.subheader(f"{course['title']} Navigation")
        
        selected_module = st.selectbox(
            "Select Module",
            options=modules,
            format_func=lambda x: x['title'],
            key=f"{course_id}_module_select"
        )
        
        if selected_module and selected_module.get('lessons'):
            selected_lesson = st.selectbox(
                "Select Lesson",
                options=selected_module['lessons'],
                format_func=lambda x: x['title'],
                key=f"{course_id}_lesson_select"
            )
        else:
            selected_lesson = None
    
    # Main content area
    if selected_lesson:
        show_lesson_content(course_id, selected_module, selected_lesson)
    else:
        show_course_overview(course_id, course, modules)

def show_course_overview(course_id, course, modules):
    """Show course overview with module list"""
    
    st.subheader("📋 Course Modules")
    
    for i, module in enumerate(modules, 1):
        with st.expander(f"Module {i}: {module['title']}", expanded=i==1):
            st.markdown(f"**Lessons in this module:** {len(module.get('lessons', []))}")
            
            if module.get('lessons'):
                for j, lesson in enumerate(module['lessons'], 1):
                    st.markdown(f"{j}. {lesson['title']}")
    
    # Course evaluation section
    st.subheader("📝 Course Evaluation")
    
    with st.form(f"course_eval_{course_id}"):
        st.markdown("Help us improve this course by providing your feedback:")
        
        rating = st.slider("Overall Rating", 1, 5, 3)
        difficulty_rating = st.slider("Difficulty Rating", 1, 5, 3)
        feedback = st.text_area("Your Feedback", placeholder="What did you like? What could be improved?")
        recommend = st.checkbox("Would you recommend this course to others?")
        
        if st.form_submit_button("Submit Evaluation"):
            evaluation_data = {
                'course_id': course_id,
                'rating': rating,
                'difficulty_rating': difficulty_rating,
                'feedback': feedback,
                'recommend': recommend
            }
            
            from utils.database import save_course_evaluation
            save_course_evaluation(evaluation_data)
            
            st.success("Thank you for your feedback!")
            
            # Log activity
            log_user_activity('course_evaluation', {
                'course_id': course_id,
                'rating': rating
            })

def show_lesson_content(course_id, module, lesson):
    """Display individual lesson content"""
    
    st.subheader(f"📖 {lesson['title']}")
    
    # Log lesson view
    log_user_activity('lesson_viewed', {
        'course_id': course_id,
        'module_id': module['id'],
        'lesson_id': lesson['id']
    })
    
    # Lesson content
    if lesson.get('content'):
        # Convert markdown to HTML and display
        lesson_html = markdown.markdown(lesson['content'], extensions=['codehilite', 'fenced_code'])
        st.markdown(lesson_html, unsafe_allow_html=True)
    
    st.divider()
    
    # Exercises section
    if lesson.get('exercises'):
        st.subheader("💻 Practice Exercises")
        
        for i, exercise in enumerate(lesson['exercises'], 1):
            with st.expander(f"Exercise {i}: {exercise['title']}", expanded=True):
                st.markdown(f"**Description:** {exercise['description']}")
                
                # Code editor
                exercise_key = f"{course_id}_{module['id']}_{lesson['id']}_ex_{i}"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Use text area as code editor (streamlit-ace would be better but not in requirements)
                    code = st.text_area(
                        "Your Code:",
                        value=exercise.get('starter_code', ''),
                        height=200,
                        key=f"{exercise_key}_code"
                    )
                
                with col2:
                    language = 'python' if course_id == 'python' else 'perl'
                    
                    if st.button("Run Code", key=f"{exercise_key}_run"):
                        if code.strip():
                            # Execute code
                            result = code_executor.execute_code(code, language)
                            
                            # Display results
                            if result['success']:
                                st.success("✅ Code executed successfully!")
                                if result['output']:
                                    st.code(result['output'], language='text')
                            else:
                                st.error("❌ Execution failed")
                                if result['error']:
                                    st.code(result['error'], language='text')
                            
                            # Get AI feedback
                            if st.button("Get AI Feedback", key=f"{exercise_key}_ai"):
                                try:
                                    ai_feedback = ai_assistant.analyze_code(code, language)
                                    show_ai_feedback(ai_feedback)
                                    
                                    # Save submission
                                    save_code_submission({
                                        'language': language,
                                        'code': code,
                                        'exercise_id': exercise_key,
                                        'result': result,
                                        'ai_feedback': ai_feedback
                                    })
                                    
                                except Exception as e:
                                    st.error(f"AI feedback unavailable: {str(e)}")
                        else:
                            st.warning("Please enter some code to run.")
                    
                    if st.button("Show Solution", key=f"{exercise_key}_solution"):
                        if exercise.get('solution'):
                            st.code(exercise['solution'], language=language)
                        else:
                            st.info("No solution available for this exercise.")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous Lesson", key=f"prev_{lesson['id']}"):
            # Logic to navigate to previous lesson
            st.info("Previous lesson navigation would be implemented here")
    
    with col2:
        if st.button("✅ Mark as Completed", use_container_width=True):
            log_user_activity('lesson_completed', {
                'course_id': course_id,
                'module_id': module['id'],
                'lesson_id': lesson['id']
            })
            
            # Update progress
            from utils.auth import update_user_progress
            update_user_progress('lessons_completed')
            
            st.success("Lesson marked as completed! 🎉")
    
    with col3:
        if st.button("Next Lesson ➡️", key=f"next_{lesson['id']}"):
            # Logic to navigate to next lesson
            st.info("Next lesson navigation would be implemented here")

def show_ai_feedback(feedback):
    """Display AI code analysis feedback"""
    
    st.subheader("🤖 AI Code Analysis")
    
    # Code quality score
    if feedback.get('code_quality_score'):
        score = feedback['code_quality_score']
        if str(score).replace('.', '').isdigit():
            st.metric("Code Quality Score", f"{score}/10")
    
    # Feedback sections
    if feedback.get('syntax_errors'):
        st.error("**Syntax Errors:**")
        for error in feedback['syntax_errors']:
            st.markdown(f"- {error}")
    
    if feedback.get('logic_issues'):
        st.warning("**Logic Issues:**")
        for issue in feedback['logic_issues']:
            st.markdown(f"- {issue}")
    
    if feedback.get('improvements'):
        st.info("**Suggested Improvements:**")
        for improvement in feedback['improvements']:
            st.markdown(f"- {improvement}")
    
    if feedback.get('best_practices'):
        st.success("**Best Practices:**")
        for practice in feedback['best_practices']:
            st.markdown(f"- {practice}")
    
    if feedback.get('overall_feedback'):
        st.markdown(f"**Overall Assessment:** {feedback['overall_feedback']}")

if __name__ == "__main__":
    main()
