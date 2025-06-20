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
```

This simple program demonstrates Python's clean syntax. The `print()` function outputs text to the console.
                        ''',
                        'exercises': [
                            {
                                'title': 'Hello World Exercise',
                                'description': 'Write a Python program that prints "Hello, World!" to the console.',
                                'starter_code': '# Write your code here\n',
                                'solution': 'print("Hello, World!")'
                            }
                        ]
                    }
                ]
            }
        ]
    
    def _get_perl_modules(self) -> List[Dict]:
        """Get PERL course modules"""
        return [
            {
                'id': 'perl_basics',
                'title': 'PERL Basics', 
                'lessons': [
                    {
                        'id': 'introduction',
                        'title': 'Introduction to PERL',
                        'content': '''
# Introduction to PERL

PERL (Practical Extraction and Reporting Language) is a powerful scripting language excellent for text processing.

## Key Features
- Powerful regular expressions
- Flexible syntax
- Rich library (CPAN)
- Cross-platform support

## Your First PERL Program
```perl
#!/usr/bin/perl
print "Hello, World!\\n";
```
                        ''',
                        'exercises': [
                            {
                                'title': 'Hello World Exercise',
                                'description': 'Write a PERL program that prints "Hello, World!" to the console.',
                                'starter_code': '#!/usr/bin/perl\n# Write your code here\n',
                                'solution': '#!/usr/bin/perl\nprint "Hello, World!\\n";'
                            }
                        ]
                    }
                ]
            }
        ]
    
    def get_course(self, course_id: str) -> Dict:
        """Get course by ID"""
        courses = st.session_state.get('courses', {})
        return courses.get(course_id, {})

# Initialize course manager
course_manager = CourseManager()
