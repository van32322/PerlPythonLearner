import streamlit as st
from datetime import datetime
from utils.auth import check_authentication, get_current_user
from utils.ai_services import ai_assistant
from utils.database import log_user_activity

# Page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access the AI chatbot.")
        return
    
    st.title("🤖 AI Learning Assistant")
    st.markdown("Get instant help with your programming questions, code debugging, and concept explanations!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        # Add welcome message
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': "👋 Hello! I'm your AI programming tutor. I can help you with Python and PERL programming questions, explain concepts, debug code, or provide coding guidance. What would you like to learn about today?",
            'timestamp': datetime.now()
        })
    
    # Sidebar with chat options
    with st.sidebar:
        st.subheader("💬 Chat Options")
        
        # Language focus
        language_focus = st.selectbox(
            "Focus on Language:",
            ["General", "Python", "PERL"],
            index=0
        )
        
        # Quick question templates
        st.subheader("⚡ Quick Questions")
        
        quick_questions = {
            "Python": [
                "Explain Python lists vs tuples",
                "How do Python decorators work?",
                "What are lambda functions?",
                "Explain Python's GIL",
                "How to handle exceptions in Python?"
            ],
            "PERL": [
                "Explain PERL regular expressions",
                "What are PERL references?",
                "How do PERL hashes work?",
                "Explain PERL subroutines",
                "What is PERL's strict pragma?"
            ],
            "General": [
                "Explain object-oriented programming",
                "What are data structures?",
                "How does recursion work?",
                "Explain algorithms vs data structures",
                "What are design patterns?"
            ]
        }
        
        selected_questions = quick_questions.get(language_focus, [])
        
        for question in selected_questions:
            if st.button(question, key=f"quick_{question}", use_container_width=True):
                # Add question to chat
                add_user_message(question)
                # Get AI response
                get_ai_response(question, language_focus.lower())
                st.rerun()
        
        st.divider()
        
        # Chat management
        st.subheader("🔧 Chat Management")
        
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("Export Chat", use_container_width=True):
            export_chat_history()
        
        # Chat statistics
        st.subheader("📊 Chat Stats")
        total_messages = len(st.session_state.chat_history)
        user_messages = len([msg for msg in st.session_state.chat_history if msg['role'] == 'user'])
        
        st.metric("Total Messages", total_messages)
        st.metric("Your Questions", user_messages)
    
    # Main chat interface
    show_chat_interface(language_focus)
    
    # Log chatbot usage
    log_user_activity('chatbot_session', {
        'language_focus': language_focus.lower(),
        'message_count': len(st.session_state.chat_history)
    })

def show_chat_interface(language_focus):
    """Display the main chat interface"""
    
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                # User message
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message['content'])
                    st.caption(f"📅 {message['timestamp'].strftime('%H:%M:%S')}")
            else:
                # Assistant message
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message['content'])
                    st.caption(f"📅 {message['timestamp'].strftime('%H:%M:%S')}")
    
    # Chat input
    st.divider()
    
    # Create columns for input and options
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your question here:",
            height=100,
            placeholder="Ask me anything about Python, PERL, or programming in general..."
        )
    
    with col2:
        st.write(" ")  # Spacing
        send_button = st.button("Send 📤", use_container_width=True)
        
        # Code analysis option
        analyze_code = st.checkbox("Include code analysis", help="Check this if you're asking about specific code")
    
    # Handle user input
    if send_button and user_input.strip():
        # Add user message
        add_user_message(user_input)
        
        # Get AI response
        context = "code analysis requested" if analyze_code else ""
        get_ai_response(user_input, language_focus.lower(), context)
        
        # Clear input and refresh
        st.rerun()
    
    elif send_button:
        st.warning("Please enter a question or message.")
    
    # Special code debugging section
    st.divider()
    st.subheader("🐛 Code Debugging Assistant")
    
    with st.expander("Debug Your Code", expanded=False):
        debug_language = st.selectbox("Select Language:", ["Python", "PERL"], key="debug_lang")
        debug_code = st.text_area("Paste your code here:", height=200, key="debug_code")
        debug_issue = st.text_input("Describe the issue (optional):", key="debug_issue")
        
        if st.button("Get Debug Help", key="debug_help"):
            if debug_code.strip():
                debug_question = f"Please help me debug this {debug_language} code:\n\n```{debug_language.lower()}\n{debug_code}\n```"
                if debug_issue:
                    debug_question += f"\n\nThe issue I'm experiencing: {debug_issue}"
                
                # Add to chat
                add_user_message(debug_question)
                get_ai_response(debug_question, debug_language.lower(), "code debugging")
                st.rerun()
            else:
                st.warning("Please paste your code first.")

def add_user_message(content):
    """Add user message to chat history"""
    st.session_state.chat_history.append({
        'role': 'user',
        'content': content,
        'timestamp': datetime.now()
    })

def get_ai_response(user_message, language="python", context=""):
    """Get AI response and add to chat history"""
    try:
        with st.spinner("🤖 Thinking..."):
            response = ai_assistant.get_chatbot_response(
                user_message=user_message,
                context=context,
                language=language
            )
        
        # Add AI response to chat
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
    except Exception as e:
        error_message = f"I apologize, but I'm having trouble right now. Please try again later. Error: {str(e)}"
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': error_message,
            'timestamp': datetime.now()
        })

def export_chat_history():
    """Export chat history as downloadable text"""
    if not st.session_state.chat_history:
        st.warning("No chat history to export.")
        return
    
    # Create formatted text
    export_text = "AI Learning Assistant - Chat History\n"
    export_text += "=" * 40 + "\n\n"
    
    for message in st.session_state.chat_history:
        role = "You" if message['role'] == 'user' else "AI Assistant"
        timestamp = message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        content = message['content']
        
        export_text += f"[{timestamp}] {role}:\n{content}\n\n"
    
    # Provide download
    st.download_button(
        label="Download Chat History",
        data=export_text,
        file_name=f"ai_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# Sample conversation starters for new users
def show_conversation_starters():
    """Show conversation starter suggestions"""
    st.subheader("💭 Conversation Starters")
    
    starters = [
        "I'm new to programming. Where should I start?",
        "What's the difference between Python and PERL?",
        "Can you explain how functions work?",
        "I'm getting an error in my code. Can you help?",
        "What are the best practices for writing clean code?",
        "How do I choose between different data structures?",
        "Can you explain object-oriented programming concepts?"
    ]
    
    cols = st.columns(2)
    for i, starter in enumerate(starters):
        col = cols[i % 2]
        with col:
            if st.button(starter, key=f"starter_{i}"):
                add_user_message(starter)
                get_ai_response(starter, "python")
                st.rerun()

if __name__ == "__main__":
    main()
