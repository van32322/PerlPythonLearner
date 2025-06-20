import streamlit as st
import time
from datetime import datetime
from utils.auth import check_authentication, get_current_user, update_user_progress
from utils.ai_services import ai_assistant
from utils.database import save_quiz_result, log_user_activity

# Page configuration
st.set_page_config(page_title="Quizzes", page_icon="📝", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access quizzes.")
        return
    
    st.title("📝 Interactive Quizzes")
    st.markdown("Test your knowledge with AI-generated questions tailored to your learning level!")
    
    # Quiz selection interface
    if 'current_quiz' not in st.session_state:
        show_quiz_selection()
    else:
        show_quiz_interface()

def show_quiz_selection():
    """Display quiz selection and configuration"""
    
    st.subheader("🎯 Create Your Quiz")
    
    # Quiz configuration form
    with st.form("quiz_config"):
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "Programming Language:",
                ["Python", "PERL"],
                index=0
            )
            
            topic = st.selectbox(
                "Topic:",
                get_topic_options(language.lower()),
                index=0
            )
            
            difficulty = st.selectbox(
                "Difficulty Level:",
                ["Beginner", "Intermediate", "Advanced"],
                index=0
            )
        
        with col2:
            question_count = st.slider(
                "Number of Questions:",
                min_value=3,
                max_value=15,
                value=5
            )
            
            quiz_type = st.selectbox(
                "Quiz Type:",
                ["Multiple Choice", "True/False", "Mixed"],
                index=0
            )
            
            time_limit = st.selectbox(
                "Time Limit:",
                ["No Limit", "5 minutes", "10 minutes", "15 minutes"],
                index=1
            )
        
        # Custom topic input
        custom_topic = st.text_input(
            "Or enter a custom topic:",
            placeholder="e.g., Python decorators, PERL regular expressions"
        )
        
        generate_button = st.form_submit_button("🚀 Generate Quiz", use_container_width=True)
    
    if generate_button:
        # Use custom topic if provided
        final_topic = custom_topic if custom_topic.strip() else topic
        
        # Generate quiz
        with st.spinner("🤖 Generating personalized quiz questions..."):
            try:
                questions = ai_assistant.generate_quiz_questions(
                    topic=final_topic,
                    language=language.lower(),
                    difficulty=difficulty.lower(),
                    count=question_count
                )
                
                if questions:
                    # Store quiz in session state
                    st.session_state.current_quiz = {
                        'questions': questions,
                        'language': language.lower(),
                        'topic': final_topic,
                        'difficulty': difficulty.lower(),
                        'time_limit': time_limit,
                        'start_time': time.time(),
                        'answers': [],
                        'current_question': 0
                    }
                    
                    st.success(f"✅ Generated {len(questions)} questions about {final_topic}!")
                    st.rerun()
                else:
                    st.error("Failed to generate quiz questions. Please try again.")
                    
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
    
    # Show recent quiz results
    show_recent_quiz_results()

def get_topic_options(language):
    """Get topic options based on programming language"""
    
    topics = {
        'python': [
            "Python Basics",
            "Variables and Data Types",
            "Control Structures",
            "Functions",
            "Lists and Tuples",
            "Dictionaries",
            "Object-Oriented Programming",
            "Exception Handling",
            "File Operations",
            "Modules and Packages",
            "Regular Expressions",
            "List Comprehensions",
            "Decorators",
            "Generators"
        ],
        'perl': [
            "PERL Basics",
            "Variables and Scalars",
            "Arrays and Hashes",
            "Regular Expressions",
            "Subroutines",
            "File Handling",
            "References",
            "Modules",
            "Object-Oriented PERL",
            "Error Handling",
            "Pattern Matching",
            "String Manipulation",
            "Control Structures"
        ]
    }
    
    return topics.get(language, ["General Programming"])

def show_quiz_interface():
    """Display the active quiz interface"""
    
    quiz = st.session_state.current_quiz
    questions = quiz['questions']
    current_q_index = quiz['current_question']
    
    if current_q_index >= len(questions):
        show_quiz_results()
        return
    
    current_question = questions[current_q_index]
    
    # Quiz header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"📝 Quiz: {quiz['topic']}")
        st.markdown(f"**Language:** {quiz['language'].title()} | **Difficulty:** {quiz['difficulty'].title()}")
    
    with col2:
        # Progress indicator
        progress = (current_q_index + 1) / len(questions)
        st.metric("Progress", f"{current_q_index + 1}/{len(questions)}")
        st.progress(progress)
    
    with col3:
        # Timer
        if quiz['time_limit'] != "No Limit":
            time_limit_minutes = int(quiz['time_limit'].split()[0])
            elapsed_time = (time.time() - quiz['start_time']) / 60
            remaining_time = max(0, time_limit_minutes - elapsed_time)
            
            st.metric("Time Left", f"{remaining_time:.1f} min")
            
            if remaining_time <= 0:
                st.error("⏰ Time's up!")
                show_quiz_results()
                return
    
    st.divider()
    
    # Question display
    st.subheader(f"Question {current_q_index + 1}")
    st.markdown(f"**{current_question['question']}**")
    
    # Answer options
    selected_answer = st.radio(
        "Select your answer:",
        options=current_question['options'],
        key=f"q_{current_q_index}_answer"
    )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_q_index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_quiz['current_question'] -= 1
                st.rerun()
    
    with col2:
        # Show explanation button (if available)
        if st.button("💡 Need a Hint?", use_container_width=True):
            if current_question.get('explanation'):
                st.info(f"💡 **Hint:** {current_question['explanation']}")
            else:
                try:
                    hint = ai_assistant.get_chatbot_response(
                        f"Give me a hint for this question: {current_question['question']}",
                        context="quiz hint",
                        language=quiz['language']
                    )
                    st.info(f"💡 **AI Hint:** {hint}")
                except:
                    st.warning("Hints not available right now.")
    
    with col3:
        if st.button("Next ➡️" if current_q_index < len(questions) - 1 else "Finish Quiz"):
            # Save answer
            answer_letter = selected_answer[0] if selected_answer else "A"
            
            # Ensure answers list is long enough
            while len(quiz['answers']) <= current_q_index:
                quiz['answers'].append("")
            
            quiz['answers'][current_q_index] = answer_letter
            
            # Move to next question or finish
            if current_q_index < len(questions) - 1:
                st.session_state.current_quiz['current_question'] += 1
                st.rerun()
            else:
                show_quiz_results()

def show_quiz_results():
    """Display quiz results and analysis"""
    
    # Add CSS to fix layout issues
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stColumn {
        overflow: visible !important;
    }
    .element-container {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    quiz = st.session_state.current_quiz
    questions = quiz['questions']
    user_answers = quiz['answers']
    
    # Calculate score
    correct_count = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        if i < len(user_answers):
            if user_answers[i] == question['correct_answer']:
                correct_count += 1
    
    score_percentage = (correct_count / total_questions) * 100
    
    # Clear any existing layout issues
    st.empty()
    
    # Display results header - full width layout
    st.balloons()
    st.title("🎉 Quiz Complete!")
    st.divider()
    
    # Score display in properly sized columns with spacing
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Score", f"{correct_count}/{total_questions}")
    
    with col2:
        st.metric("Percentage", f"{score_percentage:.1f}%")
    
    with col3:
        elapsed_time = (time.time() - quiz['start_time']) / 60
        st.metric("Time Taken", f"{elapsed_time:.1f} min")
    
    with col4:
        # Performance indicator
        if score_percentage >= 80:
            st.success("Excellent!")
        elif score_percentage >= 60:
            st.info("Good Job!")
        else:
            st.warning("Keep Practicing!")
    
    st.divider()
    
    # Detailed results section
    st.subheader("📊 Detailed Results")
    
    # Use container to ensure proper layout
    with st.container():
        for i, question in enumerate(questions):
            with st.expander(f"Question {i+1}: {'✅' if i < len(user_answers) and user_answers[i] == question['correct_answer'] else '❌'}"):
                st.markdown(f"**Question:** {question['question']}")
                
                # Show all options with indicators in a clean layout
                for option in question['options']:
                    option_letter = option[0]
                    if option_letter == question['correct_answer']:
                        st.success(f"✅ {option} (Correct Answer)")
                    elif i < len(user_answers) and option_letter == user_answers[i]:
                        st.error(f"❌ {option} (Your Answer)")
                    else:
                        st.write(option)
                
                # Show explanation
                if question.get('explanation'):
                    st.info(f"**Explanation:** {question['explanation']}")
    
    # Save results to database
    quiz_data = {
        'topic': quiz['topic'],
        'language': quiz['language'],
        'score': correct_count,
        'total_questions': total_questions,
        'time_taken': elapsed_time,
        'answers': user_answers
    }
    
    save_quiz_result(quiz_data)
    
    # Update user progress
    update_user_progress('average_quiz_score', score_percentage)
    
    # Log activity
    log_user_activity('quiz_completed', {
        'topic': quiz['topic'],
        'language': quiz['language'],
        'score': score_percentage,
        'questions': total_questions
    })
    
    # Action buttons - full width layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, key="take_another_quiz"):
            # Clear current quiz
            del st.session_state.current_quiz
            st.rerun()
    
    with col2:
        if st.button("📚 Review Topics", use_container_width=True, key="review_topics"):
            st.switch_page("pages/2_📚_Courses.py")
    
    with col3:
        if st.button("🤖 Ask AI for Help", use_container_width=True, key="ask_ai_help"):
            st.switch_page("pages/4_🤖_AI_Chatbot.py")
    
    st.divider()
    
    # Learning recommendations based on performance
    if score_percentage < 70:
        st.subheader("📖 Recommended Study Topics")
        
        try:
            recommendations = ai_assistant.get_learning_recommendations(
                user_progress={'quiz_score': score_percentage, 'weak_areas': quiz['topic']},
                current_topic=quiz['topic']
            )
            
            if recommendations:
                for rec in recommendations[:3]:
                    st.markdown(f"• {rec}")
            else:
                st.info("Practice more questions on this topic to improve your understanding.")
                
        except Exception as e:
            st.info("Focus on reviewing the questions you missed and study the explanations provided.")

def show_recent_quiz_results():
    """Show recent quiz results"""
    
    st.subheader("📈 Your Recent Quiz Results")
    
    if 'quiz_results' in st.session_state and st.session_state.quiz_results:
        # Filter results for current user
        user = get_current_user()
        user_results = [
            result for result in st.session_state.quiz_results
            if result.get('user') == user['username']
        ]
        
        if user_results:
            # Show last 5 results
            recent_results = user_results[-5:]
            
            for result in reversed(recent_results):
                score_pct = (result['score'] / result['total_questions']) * 100
                timestamp = result['timestamp'][:19].replace('T', ' ')
                
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{result['topic']}** ({result['language'].title()})")
                
                with col2:
                    st.write(f"{result['score']}/{result['total_questions']}")
                
                with col3:
                    st.write(f"{score_pct:.1f}%")
                
                with col4:
                    st.write(timestamp.split()[1][:5])  # Show time only
        else:
            st.info("No quiz results yet. Take your first quiz!")
    else:
        st.info("No quiz results yet. Take your first quiz!")

if __name__ == "__main__":
    main()
