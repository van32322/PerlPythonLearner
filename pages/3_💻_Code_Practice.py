import streamlit as st
from streamlit_ace import st_ace
from utils.auth import check_authentication, get_current_user
from utils.code_executor import code_executor
from utils.ai_services import ai_assistant
from utils.database import save_code_submission, log_user_activity

# Page configuration
st.set_page_config(page_title="Code Practice", page_icon="💻", layout="wide")

def main():
    if not check_authentication():
        st.error("Please log in to access the code practice environment.")
        return
    
    st.title("💻 Interactive Code Practice")
    st.markdown("Write, run, and get AI feedback on your Python and PERL code!")
    
    # Language selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        language = st.selectbox(
            "Choose Language:",
            options=["Python", "PERL"],
            index=0
        )
        
        # Sample code selection
        sample_options = get_sample_code_options(language.lower())
        selected_sample = st.selectbox(
            "Load Sample Code:",
            options=["Custom Code"] + list(sample_options.keys()),
            index=0
        )
        
        # Code execution settings
        st.subheader("⚙️ Settings")
        auto_save = st.checkbox("Auto-save code", value=True)
        show_line_numbers = st.checkbox("Show line numbers", value=True)
        
    with col2:
        # Main code editor area
        show_code_editor(language.lower(), selected_sample, sample_options, show_line_numbers)
    
    # Log practice session
    log_user_activity('code_practice_session', {
        'language': language.lower(),
        'sample_used': selected_sample if selected_sample != "Custom Code" else None
    })

def get_sample_code_options(language):
    """Get sample code examples for the selected language"""
    
    if language == "python":
        return {
            "Hello World": 'print("Hello, World!")',
            "Variables and Types": '''# Variables and data types
name = "Alice"
age = 25
height = 5.6
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")
print(f"Is student: {is_student}")''',
            "Lists and Loops": '''# Working with lists and loops
fruits = ["apple", "banana", "orange", "grape"]

print("Fruits in the list:")
for i, fruit in enumerate(fruits, 1):
    print(f"{i}. {fruit}")

# List comprehension
uppercase_fruits = [fruit.upper() for fruit in fruits]
print(f"Uppercase fruits: {uppercase_fruits}")''',
            "Functions": '''# Function definition and usage
def calculate_area(length, width):
    """Calculate the area of a rectangle"""
    return length * width

def greet_user(name, age=None):
    """Greet user with optional age"""
    if age:
        return f"Hello, {name}! You are {age} years old."
    else:
        return f"Hello, {name}!"

# Test the functions
area = calculate_area(5, 3)
print(f"Area: {area}")

greeting = greet_user("Alice", 25)
print(greeting)''',
            "File Handling": '''# File operations example
import tempfile
import os

# Create a temporary file for demo
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("Hello from Python!\\n")
    f.write("This is a file handling example.\\n")
    temp_filename = f.name

# Read the file
try:
    with open(temp_filename, 'r') as f:
        content = f.read()
        print("File content:")
        print(content)
finally:
    # Clean up
    os.unlink(temp_filename)'''
        }
    
    elif language == "perl":
        return {
            "Hello World": '''#!/usr/bin/perl
print "Hello, World!\\n";''',
            "Variables": '''#!/usr/bin/perl
# Scalar variables
my $name = "Alice";
my $age = 25;
my $pi = 3.14159;

# Array variables
my @colors = ("red", "green", "blue");
my @numbers = (1, 2, 3, 4, 5);

# Hash variables
my %person = (
    "name" => "Alice",
    "age" => 25,
    "city" => "New York"
);

print "Name: $name\\n";
print "Age: $age\\n";
print "Colors: @colors\\n";
print "Person age: $person{age}\\n";''',
            "Loops and Arrays": '''#!/usr/bin/perl
my @fruits = ("apple", "banana", "orange", "grape");

print "Fruits in the array:\\n";
for my $i (0..$#fruits) {
    print ($i + 1) . ". $fruits[$i]\\n";
}

print "\\nUsing foreach loop:\\n";
foreach my $fruit (@fruits) {
    print "- $fruit\\n";
}''',
            "Subroutines": '''#!/usr/bin/perl
# Subroutine definition
sub calculate_area {
    my ($length, $width) = @_;
    return $length * $width;
}

sub greet_user {
    my ($name, $age) = @_;
    if (defined $age) {
        return "Hello, $name! You are $age years old.";
    } else {
        return "Hello, $name!";
    }
}

# Test the subroutines
my $area = calculate_area(5, 3);
print "Area: $area\\n";

my $greeting = greet_user("Alice", 25);
print "$greeting\\n";''',
            "Regular Expressions": '''#!/usr/bin/perl
my $text = "The quick brown fox jumps over the lazy dog";
my $email = "user@example.com";

# Pattern matching
if ($text =~ /fox/) {
    print "Found 'fox' in the text\\n";
}

# Email validation
if ($email =~ /^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$/) {
    print "Valid email address: $email\\n";
} else {
    print "Invalid email address\\n";
}

# Substitution
my $new_text = $text;
$new_text =~ s/fox/cat/g;
print "Original: $text\\n";
print "Modified: $new_text\\n";'''
        }
    
    return {}

def show_code_editor(language, selected_sample, sample_options, show_line_numbers):
    """Display the main code editor interface"""
    
    # Load sample code if selected
    initial_code = ""
    if selected_sample != "Custom Code" and selected_sample in sample_options:
        initial_code = sample_options[selected_sample]
    
    # Use streamlit-ace for better code editing experience
    try:
        code = st_ace(
            value=initial_code,
            language=language,
            theme='monokai',
            key=f'code_editor_{language}',
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=4,
            show_gutter=show_line_numbers,
            show_print_margin=True,
            wrap=False,
            annotations=None
        )
    except:
        # Fallback to text area
        code = st.text_area(
            "Code Editor:",
            value=initial_code,
            height=400,
            key=f'code_textarea_{language}',
            help="Enter your code here"
        )
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        run_button = st.button("▶️ Run Code", use_container_width=True)
    
    with col2:
        analyze_button = st.button("🔍 Analyze Code", use_container_width=True)
    
    with col3:
        clear_button = st.button("🗑️ Clear Code", use_container_width=True)
    
    with col4:
        save_button = st.button("💾 Save Code", use_container_width=True)
    
    # Handle button actions
    if clear_button:
        st.rerun()
    
    if run_button and code.strip():
        st.subheader("📊 Execution Results")
        
        with st.spinner("Running your code..."):
            result = code_executor.execute_code(code, language)
        
        # Display execution results
        if result['success']:
            st.success("✅ Code executed successfully!")
            
            if result['output']:
                st.subheader("Output:")
                st.code(result['output'], language='text')
            else:
                st.info("Code executed without output.")
        else:
            st.error("❌ Code execution failed")
            
            if result['error']:
                st.subheader("Error:")
                st.code(result['error'], language='text')
        
        # Save execution result
        if save_button or st.session_state.get('auto_save', True):
            save_code_submission({
                'language': language,
                'code': code,
                'exercise_id': 'practice_session',
                'result': result,
                'ai_feedback': {}
            })
    
    elif run_button:
        st.warning("Please enter some code to run.")
    
    if analyze_button and code.strip():
        st.subheader("🤖 AI Code Analysis")
        
        with st.spinner("Analyzing your code..."):
            try:
                analysis = ai_assistant.analyze_code(code, language)
                show_detailed_analysis(analysis)
                
                # Save analysis
                save_code_submission({
                    'language': language,
                    'code': code,
                    'exercise_id': 'code_analysis',
                    'result': {'analysis_requested': True},
                    'ai_feedback': analysis
                })
                
            except Exception as e:
                st.error(f"AI analysis failed: {str(e)}")
    
    elif analyze_button:
        st.warning("Please enter some code to analyze.")
    
    # Code suggestions sidebar
    with st.sidebar:
        st.subheader("💡 Coding Tips")
        
        if language == "python":
            st.markdown("""
            **Python Best Practices:**
            - Use meaningful variable names
            - Follow PEP 8 style guide
            - Add docstrings to functions
            - Handle exceptions properly
            - Use list comprehensions when appropriate
            """)
        else:
            st.markdown("""
            **PERL Best Practices:**
            - Always use `strict` and `warnings`
            - Declare variables with `my`
            - Use meaningful variable names
            - Comment your regular expressions
            - Handle errors gracefully
            """)
        
        # Quick reference
        st.subheader("📚 Quick Reference")
        
        if st.button("Get Help with Concepts"):
            concept = st.text_input("Enter a concept to learn about:")
            if concept:
                try:
                    explanation = ai_assistant.explain_concept(concept, language)
                    st.markdown(explanation)
                except Exception as e:
                    st.error(f"Unable to get explanation: {str(e)}")

def show_detailed_analysis(analysis):
    """Display detailed AI code analysis"""
    
    # Code quality score
    if analysis.get('code_quality_score') and str(analysis['code_quality_score']).replace('.', '').isdigit():
        score = float(analysis['code_quality_score'])
        st.metric("Code Quality Score", f"{score}/10")
        
        # Quality indicator
        if score >= 8:
            st.success("Excellent code quality! 🌟")
        elif score >= 6:
            st.info("Good code quality with room for improvement 👍")
        elif score >= 4:
            st.warning("Code quality needs improvement ⚠️")
        else:
            st.error("Code quality needs significant improvement 🔧")
    
    # Create tabs for different types of feedback
    tabs = st.tabs(["🚨 Issues", "💡 Improvements", "✅ Best Practices", "📝 Summary"])
    
    with tabs[0]:
        # Syntax errors and logic issues
        if analysis.get('syntax_errors'):
            st.error("**Syntax Errors Found:**")
            for error in analysis['syntax_errors']:
                st.markdown(f"• {error}")
        
        if analysis.get('logic_issues'):
            st.warning("**Logic Issues:**")
            for issue in analysis['logic_issues']:
                st.markdown(f"• {issue}")
        
        if not analysis.get('syntax_errors') and not analysis.get('logic_issues'):
            st.success("No critical issues found! ✨")
    
    with tabs[1]:
        # Suggested improvements
        if analysis.get('improvements'):
            st.info("**Suggested Improvements:**")
            for improvement in analysis['improvements']:
                st.markdown(f"• {improvement}")
        else:
            st.success("No specific improvements suggested!")
    
    with tabs[2]:
        # Best practices
        if analysis.get('best_practices'):
            st.success("**Best Practice Recommendations:**")
            for practice in analysis['best_practices']:
                st.markdown(f"• {practice}")
        else:
            st.info("No specific best practices noted.")
    
    with tabs[3]:
        # Overall feedback
        if analysis.get('overall_feedback'):
            st.markdown("**Overall Assessment:**")
            st.markdown(analysis['overall_feedback'])

if __name__ == "__main__":
    main()
