"""
Python Basics Course Content
Complete course structure with lessons, exercises, and examples
"""

def get_python_course_content():
    """Return the complete Python course structure"""
    
    return {
        'title': 'Python Programming Course',
        'description': 'Comprehensive Python programming course from basics to advanced topics',
        'difficulty': 'Beginner to Advanced',
        'estimated_hours': 40,
        'modules': [
            {
                'id': 'python_basics',
                'title': 'Python Basics',
                'description': 'Introduction to Python programming fundamentals',
                'lessons': [
                    {
                        'id': 'introduction',
                        'title': 'Introduction to Python',
                        'content': '''
# Introduction to Python

Python is a high-level, interpreted programming language known for its simplicity and readability.

## Why Python?
- **Easy to learn and use**: Python's syntax is similar to English, making it beginner-friendly
- **Versatile**: Used in web development, data science, AI, automation, and more
- **Large community**: Extensive libraries and strong community support
- **Cross-platform**: Runs on Windows, macOS, Linux, and more

## Python Philosophy
The Zen of Python emphasizes:
- Beautiful is better than ugly
- Explicit is better than implicit
- Simple is better than complex
- Readability counts

## Your First Python Program
```python
print("Hello, World!")
