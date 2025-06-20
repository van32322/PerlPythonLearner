import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import check_authentication, get_current_user
from utils.course_data import course_manager
from utils.database import log_user_activity
from utils.ai_services import ai_assistant

# Page configuration
st.set_page_config(page_title="Search", page_icon="🔍", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access search functionality.")
        return
    
    st.title("🔍 Search Learning Content")
    st.markdown("Find lessons, topics, and resources across Python and PERL courses")
    
    # Search interface
    show_search_interface()
    
    # Log search page visit
    log_user_activity('search_page_visit', {'timestamp': datetime.now().isoformat()})

def show_search_interface():
    """Display the main search interface"""
    
    # Search form
    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search for topics, lessons, or concepts:",
                placeholder="e.g., Python functions, PERL arrays, loops, variables..."
            )
        
        with col2:
            st.write("")  # Spacing
            search_button = st.form_submit_button("🔍 Search", use_container_width=True)
    
    # Advanced search options
    with st.expander("🔧 Advanced Search Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            language_filter = st.selectbox(
                "Language:",
                ["All", "Python", "PERL"],
                index=0
            )
        
        with col2:
            content_type = st.selectbox(
                "Content Type:",
                ["All", "Lessons", "Exercises", "Examples"],
                index=0
            )
        
        with col3:
            difficulty_filter = st.selectbox(
                "Difficulty:",
                ["All", "Beginner", "Intermediate", "Advanced"],
                index=0
            )
    
    # Process search
    if search_button and search_query.strip():
        perform_search(search_query, language_filter, content_type, difficulty_filter)
    elif search_button:
        st.warning("Please enter a search term.")
    
    # Quick search suggestions
    show_search_suggestions()
    
    # Recent searches
    show_recent_searches()

def perform_search(query, language_filter, content_type, difficulty_filter):
    """Perform search across course content"""
    
    st.subheader(f"🔍 Search Results for: '{query}'")
    
    # Log search activity
    log_user_activity('search_performed', {
        'query': query,
        'language_filter': language_filter,
        'content_type': content_type,
        'difficulty_filter': difficulty_filter
    })
    
    # Store recent search
    store_recent_search(query, language_filter)
    
    # Search through courses
    search_results = search_course_content(query, language_filter, content_type, difficulty_filter)
    
    if not search_results:
        st.info("No results found. Try different search terms or check the suggestions below.")
        
        # AI-powered search suggestions
        try:
            with st.spinner("🤖 Getting AI-powered search suggestions..."):
                suggestions = ai_assistant.get_search_suggestions(query, language_filter.lower())
                
                if suggestions:
                    st.subheader("💡 Did you mean?")
                    for suggestion in suggestions[:5]:
                        if st.button(f"🔍 {suggestion}", key=f"suggest_{suggestion}"):
                            st.session_state.search_suggestion = suggestion
                            st.rerun()
        except Exception as e:
            st.warning("Unable to generate search suggestions at this time.")
        
        return
    
    # Display search results
    st.success(f"Found {len(search_results)} results")
    
    # Group results by type
    lessons = [r for r in search_results if r['type'] == 'lesson']
    exercises = [r for r in search_results if r['type'] == 'exercise']
    examples = [r for r in search_results if r['type'] == 'example']
    
    # Display results in tabs
    tabs = st.tabs([f"📚 Lessons ({len(lessons)})", f"💻 Exercises ({len(exercises)})", f"📝 Examples ({len(examples)})"])
    
    with tabs[0]:
        display_lesson_results(lessons)
    
    with tabs[1]:
        display_exercise_results(exercises)
    
    with tabs[2]:
        display_example_results(examples)

def search_course_content(query, language_filter, content_type, difficulty_filter):
    """Search through course content and return matching results"""
    
    results = []
    query_lower = query.lower()
    
    # Get all courses
    courses = st.session_state.get('courses', {})
    
    for course_id, course in courses.items():
        # Apply language filter
        if language_filter != "All" and course_id != language_filter.lower():
            continue
        
        # Search through modules and lessons
        for module in course.get('modules', []):
            for lesson in module.get('lessons', []):
                # Search in lesson title and content
                if (query_lower in lesson.get('title', '').lower() or 
                    query_lower in lesson.get('content', '').lower()):
                    
                    # Apply content type filter
                    if content_type == "All" or content_type == "Lessons":
                        results.append({
                            'type': 'lesson',
                            'title': lesson.get('title', ''),
                            'content': lesson.get('content', '')[:200] + '...',
                            'language': course_id,
                            'module': module.get('title', ''),
                            'course': course.get('title', ''),
                            'lesson_id': lesson.get('id', ''),
                            'module_id': module.get('id', '')
                        })
                
                # Search through exercises
                for exercise in lesson.get('exercises', []):
                    if (query_lower in exercise.get('title', '').lower() or 
                        query_lower in exercise.get('description', '').lower()):
                        
                        if content_type == "All" or content_type == "Exercises":
                            results.append({
                                'type': 'exercise',
                                'title': exercise.get('title', ''),
                                'content': exercise.get('description', ''),
                                'language': course_id,
                                'module': module.get('title', ''),
                                'course': course.get('title', ''),
                                'lesson_title': lesson.get('title', ''),
                                'lesson_id': lesson.get('id', ''),
                                'module_id': module.get('id', '')
                            })
    
    # Search through sample code and examples
    examples = get_code_examples()
    for example in examples.get(language_filter.lower(), []) if language_filter != "All" else [item for sublist in examples.values() for item in sublist]:
        if (query_lower in example.get('title', '').lower() or 
            query_lower in example.get('description', '').lower() or 
            query_lower in example.get('code', '').lower()):
            
            if content_type == "All" or content_type == "Examples":
                results.append({
                    'type': 'example',
                    'title': example.get('title', ''),
                    'content': example.get('description', ''),
                    'code': example.get('code', ''),
                    'language': example.get('language', ''),
                    'category': example.get('category', '')
                })
    
    return results

def display_lesson_results(lessons):
    """Display lesson search results"""
    
    if not lessons:
        st.info("No lessons found matching your search criteria.")
        return
    
    for lesson in lessons:
        with st.expander(f"📚 {lesson['title']} ({lesson['language'].title()})"):
            st.markdown(f"**Course:** {lesson['course']}")
            st.markdown(f"**Module:** {lesson['module']}")
            st.markdown(f"**Content Preview:** {lesson['content']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📖 View Lesson", key=f"view_lesson_{lesson['lesson_id']}"):
                    # Navigate to lesson (would need proper navigation logic)
                    st.info(f"Navigation to {lesson['title']} would be implemented here")
            
            with col2:
                if st.button(f"📚 Go to Course", key=f"view_course_{lesson['lesson_id']}"):
                    st.switch_page("pages/2_📚_Courses.py")

def display_exercise_results(exercises):
    """Display exercise search results"""
    
    if not exercises:
        st.info("No exercises found matching your search criteria.")
        return
    
    for exercise in exercises:
        with st.expander(f"💻 {exercise['title']} ({exercise['language'].title()})"):
            st.markdown(f"**Course:** {exercise['course']}")
            st.markdown(f"**Module:** {exercise['module']}")
            st.markdown(f"**Lesson:** {exercise['lesson_title']}")
            st.markdown(f"**Description:** {exercise['content']}")
            
            if st.button(f"🏃‍♂️ Start Exercise", key=f"start_ex_{exercise['lesson_id']}"):
                st.switch_page("pages/3_💻_Code_Practice.py")

def display_example_results(examples):
    """Display code example search results"""
    
    if not examples:
        st.info("No code examples found matching your search criteria.")
        return
    
    for example in examples:
        with st.expander(f"📝 {example['title']} ({example['language'].title()})"):
            st.markdown(f"**Category:** {example.get('category', 'General')}")
            st.markdown(f"**Description:** {example['content']}")
            
            if example.get('code'):
                st.code(example['code'], language=example['language'].lower())
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"💻 Try in Editor", key=f"try_example_{example['title']}"):
                    # Store example code for practice page
                    st.session_state.example_code = example.get('code', '')
                    st.session_state.example_language = example['language'].lower()
                    st.switch_page("pages/3_💻_Code_Practice.py")
            
            with col2:
                if st.button(f"🤖 Explain Code", key=f"explain_{example['title']}"):
                    try:
                        explanation = ai_assistant.get_chatbot_response(
                            f"Please explain this {example['language']} code:\n\n{example.get('code', '')}",
                            context="code explanation",
                            language=example['language'].lower()
                        )
                        st.info(f"**AI Explanation:** {explanation}")
                    except Exception as e:
                        st.error("Unable to get AI explanation at this time.")

def get_code_examples():
    """Get code examples for search"""
    
    return {
        'python': [
            {
                'title': 'Hello World',
                'description': 'Basic Python program to print Hello World',
                'code': 'print("Hello, World!")',
                'language': 'python',
                'category': 'Basics'
            },
            {
                'title': 'List Comprehension',
                'description': 'Create lists using comprehension syntax',
                'code': 'squares = [x**2 for x in range(10)]\nprint(squares)',
                'language': 'python',
                'category': 'Data Structures'
            },
            {
                'title': 'Function Definition',
                'description': 'How to define and call functions in Python',
                'code': '''def greet(name):
    return f"Hello, {name}!"

message = greet("Alice")
print(message)''',
                'language': 'python',
                'category': 'Functions'
            }
        ],
        'perl': [
            {
                'title': 'Hello World',
                'description': 'Basic PERL program to print Hello World',
                'code': '#!/usr/bin/perl\nprint "Hello, World!\\n";',
                'language': 'perl',
                'category': 'Basics'
            },
            {
                'title': 'Array Operations',
                'description': 'Working with arrays in PERL',
                'code': '''my @fruits = ("apple", "banana", "orange");
print "Fruits: @fruits\\n";
push @fruits, "grape";
print "Updated: @fruits\\n";''',
                'language': 'perl',
                'category': 'Data Structures'
            },
            {
                'title': 'Regular Expression',
                'description': 'Pattern matching with regular expressions',
                'code': '''my $text = "The email is user@example.com";
if ($text =~ /([\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,})/) {
    print "Found email: $1\\n";
}''',
                'language': 'perl',
                'category': 'Pattern Matching'
            }
        ]
    }

def show_search_suggestions():
    """Show quick search suggestions"""
    
    st.subheader("💡 Popular Search Topics")
    
    suggestions = {
        'Python': [
            'functions', 'lists', 'dictionaries', 'loops', 'classes',
            'exceptions', 'file operations', 'list comprehensions'
        ],
        'PERL': [
            'arrays', 'hashes', 'subroutines', 'regular expressions',
            'references', 'modules', 'pattern matching'
        ],
        'General': [
            'variables', 'conditionals', 'data types', 'algorithms',
            'debugging', 'best practices', 'object oriented'
        ]
    }
    
    tabs = st.tabs(['🐍 Python', '🔤 PERL', '📖 General'])
    
    for i, (category, topics) in enumerate(suggestions.items()):
        with tabs[i]:
            cols = st.columns(4)
            for j, topic in enumerate(topics):
                col = cols[j % 4]
                with col:
                    if st.button(f"🔍 {topic}", key=f"suggest_{category}_{topic}"):
                        # Trigger search with this topic
                        st.session_state.suggested_search = topic
                        st.rerun()

def show_recent_searches():
    """Show recent search history"""
    
    st.subheader("🕒 Recent Searches")
    
    if 'recent_searches' not in st.session_state:
        st.session_state.recent_searches = []
    
    if not st.session_state.recent_searches:
        st.info("No recent searches yet.")
        return
    
    # Show last 5 searches
    recent = st.session_state.recent_searches[-5:]
    
    for i, search in enumerate(reversed(recent)):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if st.button(f"🔍 {search['query']}", key=f"recent_{i}"):
                # Repeat this search
                perform_search(search['query'], search['language'], "All", "All")
        
        with col2:
            st.text(search['language'])
        
        with col3:
            timestamp = pd.to_datetime(search['timestamp'])
            st.text(timestamp.strftime('%m/%d %H:%M'))

def store_recent_search(query, language):
    """Store search in recent searches"""
    
    if 'recent_searches' not in st.session_state:
        st.session_state.recent_searches = []
    
    # Add new search
    search_entry = {
        'query': query,
        'language': language,
        'timestamp': datetime.now().isoformat()
    }
    
    # Remove duplicate if exists
    st.session_state.recent_searches = [
        s for s in st.session_state.recent_searches 
        if s['query'].lower() != query.lower()
    ]
    
    # Add to front and limit to 10
    st.session_state.recent_searches.append(search_entry)
    st.session_state.recent_searches = st.session_state.recent_searches[-10:]

if __name__ == "__main__":
    main()
