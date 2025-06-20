"""
PERL Basics Course Content
Complete course structure with lessons, exercises, and examples
"""

def get_perl_course_content():
    """Return the complete PERL course structure"""
    
    return {
        'title': 'PERL Programming Course',
        'description': 'Complete PERL programming course covering essential concepts and practical applications',
        'difficulty': 'Beginner to Intermediate',
        'estimated_hours': 30,
        'modules': [
            {
                'id': 'perl_introduction',
                'title': 'PERL Introduction',
                'description': 'Getting started with PERL programming',
                'lessons': [
                    {
                        'id': 'what_is_perl',
                        'title': 'What is PERL?',
                        'content': '''
# What is PERL?

PERL (Practical Extraction and Reporting Language) is a high-level, interpreted programming language originally developed for text processing.

## History and Purpose
- Created by Larry Wall in 1987
- Originally designed for text manipulation and system administration
- Known for its powerful regular expression capabilities
- Philosophy: "There's more than one way to do it" (TMTOWTDI)

## Key Features
- **Powerful regular expressions**: Built-in pattern matching
- **Flexible syntax**: Multiple ways to accomplish tasks
- **Rich library**: CPAN (Comprehensive Perl Archive Network)
- **Cross-platform**: Runs on Unix, Linux, Windows, Mac
- **Interpreted**: No compilation step needed

## PERL's Strengths
- Text processing and manipulation
- System administration scripts
- Bioinformatics and data mining
- Legacy system maintenance
- Quick and dirty scripting

## Basic PERL Program Structure
```perl
#!/usr/bin/perl
use strict;
use warnings;

print "Hello, World!\\n";
