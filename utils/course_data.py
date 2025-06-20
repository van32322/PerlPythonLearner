from typing import Dict, List
import streamlit as st

class CourseManager:
    """Manages course content and structure"""
    
    def __init__(self):
        self.initialize_courses()
    
    def initialize_courses(self):
        """Initialize course data structure"""
        if 'courses' not in st.session_state:
            st.session_state.courses = {
                'python': {
                    'title': 'Python Programming Course',
                    'description': 'Comprehensive Python programming course from basics to advanced topics',
                    'difficulty': 'Beginner to Advanced',
                    'estimated_hours': 40,
                    'modules': self._get_python_modules()
                },
                'perl': {
                    'title': 'PERL Programming Course',
                    'description': 'Complete PERL programming course covering essential concepts and practical applications',
                    'difficulty': 'Beginner to Intermediate',
                    'estimated_hours': 30,
                    'modules': self._get_perl_modules()
                }
            }
    
    def _get_python_modules(self) -> List[Dict]:
        """Get Python course modules"""
        return [
            {
                'id': 'python_basics',
                'title': 'Python Basics',
                'lessons': [
                    {
                        'id': 'introduction',
                        'title': 'Introduction to Python',
                        'content': '''
# Introduction to Python

Python is a high-level, interpreted programming language known for its simplicity and readability.

## Why Python?
- Easy to learn and use
- Versatile (web development, data science, AI, automation)
- Large community and extensive libraries
- Cross-platform compatibility

## Python Philosophy
"Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex."

## Your First Python Program
```python
print("Hello, World!")
