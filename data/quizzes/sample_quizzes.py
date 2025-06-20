"""
Sample Quiz Questions for Python and PERL courses
Used as fallback when AI quiz generation is unavailable
"""

def get_sample_quiz_questions():
    """Return sample quiz questions organized by language and topic"""
    
    return {
        'python': {
            'basics': [
                {
                    'question': 'What is the correct way to print "Hello, World!" in Python?',
                    'options': [
                        'A) print("Hello, World!")',
                        'B) echo "Hello, World!"',
                        'C) console.log("Hello, World!")',
                        'D) printf("Hello, World!")'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'The print() function is used to display output in Python.'
                },
                {
                    'question': 'Which of the following is a valid Python variable name?',
                    'options': [
                        'A) 2variable',
                        'B) variable-name',
                        'C) variable_name',
                        'D) variable name'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Python variable names can contain letters, numbers, and underscores, but cannot start with a number or contain spaces/hyphens.'
                },
                {
                    'question': 'What data type is the result of: type(3.14)?',
                    'options': [
                        'A) int',
                        'B) float',
                        'C) str',
                        'D) decimal'
                    ],
                    'correct_answer': 'B',
                    'explanation': '3.14 is a floating-point number, so type() returns <class "float">.'
                },
                {
                    'question': 'How do you create a comment in Python?',
                    'options': [
                        'A) // This is a comment',
                        'B) /* This is a comment */',
                        'C) # This is a comment',
                        'D) <!-- This is a comment -->'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Python uses the # symbol for single-line comments.'
                },
                {
                    'question': 'Which operator is used for string concatenation in Python?',
                    'options': [
                        'A) &',
                        'B) +',
                        'C) .',
                        'D) *'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The + operator concatenates strings in Python. Example: "Hello" + " World" = "Hello World"'
                }
            ],
            'data_structures': [
                {
                    'question': 'How do you access the last element of a list in Python?',
                    'options': [
                        'A) list[last]',
                        'B) list[-1]',
                        'C) list[end]',
                        'D) list[length-1]'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'Python supports negative indexing, where -1 refers to the last element.'
                },
                {
                    'question': 'What is the difference between a list and a tuple in Python?',
                    'options': [
                        'A) Lists are ordered, tuples are not',
                        'B) Lists are mutable, tuples are immutable',
                        'C) Lists use [], tuples use {}',
                        'D) There is no difference'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'Lists can be modified after creation (mutable), while tuples cannot be changed (immutable).'
                },
                {
                    'question': 'How do you add an element to the end of a list?',
                    'options': [
                        'A) list.add(element)',
                        'B) list.push(element)',
                        'C) list.append(element)',
                        'D) list.insert(element)'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'The append() method adds an element to the end of a list.'
                },
                {
                    'question': 'What does the following list comprehension do: [x**2 for x in range(5)]?',
                    'options': [
                        'A) Creates [0, 1, 4, 9, 16]',
                        'B) Creates [1, 4, 9, 16, 25]',
                        'C) Creates [0, 1, 2, 3, 4]',
                        'D) Creates an error'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'This creates a list of squares for numbers 0-4: [0², 1², 2², 3², 4²] = [0, 1, 4, 9, 16]'
                },
                {
                    'question': 'How do you get all the keys from a dictionary?',
                    'options': [
                        'A) dict.keys()',
                        'B) dict.getKeys()',
                        'C) keys(dict)',
                        'D) dict.allKeys()'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'The keys() method returns a view of all keys in the dictionary.'
                }
            ],
            'functions': [
                {
                    'question': 'What keyword is used to define a function in Python?',
                    'options': [
                        'A) function',
                        'B) def',
                        'C) func',
                        'D) define'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The "def" keyword is used to define functions in Python.'
                },
                {
                    'question': 'What does a function return by default if no return statement is specified?',
                    'options': [
                        'A) 0',
                        'B) ""',
                        'C) None',
                        'D) False'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Python functions return None by default if no explicit return statement is provided.'
                },
                {
                    'question': 'How do you call a function named "greet" with argument "Alice"?',
                    'options': [
                        'A) greet("Alice")',
                        'B) call greet("Alice")',
                        'C) greet["Alice"]',
                        'D) greet.call("Alice")'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'Functions are called by using the function name followed by parentheses containing arguments.'
                },
                {
                    'question': 'What is *args used for in function parameters?',
                    'options': [
                        'A) To pass keyword arguments',
                        'B) To pass a variable number of positional arguments',
                        'C) To make arguments optional',
                        'D) To pass arguments by reference'
                    ],
                    'correct_answer': 'B',
                    'explanation': '*args allows a function to accept any number of positional arguments as a tuple.'
                },
                {
                    'question': 'What is a lambda function?',
                    'options': [
                        'A) A function that takes lambda as parameter',
                        'B) A built-in Python function',
                        'C) An anonymous function',
                        'D) A function that returns lambda'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Lambda functions are anonymous functions defined inline using the lambda keyword.'
                }
            ]
        },
        'perl': {
            'basics': [
                {
                    'question': 'What character is used to prefix scalar variables in PERL?',
                    'options': [
                        'A) @',
                        'B) %',
                        'C) $',
                        'D) &'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Scalar variables in PERL are prefixed with the $ sigil.'
                },
                {
                    'question': 'Which pragma enforces good programming practices in PERL?',
                    'options': [
                        'A) use warnings',
                        'B) use strict',
                        'C) use safe',
                        'D) use standard'
                    ],
                    'correct_answer': 'B',
                    'explanation': '"use strict" enforces strict variable declarations and other good practices.'
                },
                {
                    'question': 'How do you print output in PERL?',
                    'options': [
                        'A) echo "Hello"',
                        'B) print "Hello"',
                        'C) printf("Hello")',
                        'D) display "Hello"'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The print function is used to output text in PERL.'
                },
                {
                    'question': 'What does the shebang line #!/usr/bin/perl do?',
                    'options': [
                        'A) It\'s a comment',
                        'B) It specifies the PERL interpreter path',
                        'C) It imports a module',
                        'D) It defines a variable'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The shebang line tells the system which interpreter to use to execute the script.'
                },
                {
                    'question': 'Which operator is used for string concatenation in PERL?',
                    'options': [
                        'A) +',
                        'B) &',
                        'C) .',
                        'D) ||'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'The dot (.) operator concatenates strings in PERL.'
                }
            ],
            'variables': [
                {
                    'question': 'What sigil is used for arrays in PERL?',
                    'options': [
                        'A) $',
                        'B) @',
                        'C) %',
                        'D) &'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'Arrays in PERL are prefixed with the @ sigil.'
                },
                {
                    'question': 'How do you access the first element of an array @fruits?',
                    'options': [
                        'A) @fruits[0]',
                        'B) $fruits[0]',
                        'C) fruits[0]',
                        'D) @fruits{0}'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'Individual array elements are accessed with $ sigil because they are scalars.'
                },
                {
                    'question': 'What sigil is used for hashes in PERL?',
                    'options': [
                        'A) $',
                        'B) @',
                        'C) %',
                        'D) #'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'Hashes in PERL are prefixed with the % sigil.'
                },
                {
                    'question': 'How do you get the number of elements in an array @arr?',
                    'options': [
                        'A) length(@arr)',
                        'B) @arr.length',
                        'C) scalar(@arr)',
                        'D) size(@arr)'
                    ],
                    'correct_answer': 'C',
                    'explanation': 'scalar(@arr) returns the number of elements in an array by forcing scalar context.'
                },
                {
                    'question': 'What does "my" keyword do in PERL?',
                    'options': [
                        'A) Creates a global variable',
                        'B) Creates a lexically scoped variable',
                        'C) Creates a constant',
                        'D) Creates a reference'
                    ],
                    'correct_answer': 'B',
                    'explanation': '"my" creates lexically scoped variables that are only visible in the current block.'
                }
            ],
            'regex': [
                {
                    'question': 'Which operator is used for pattern matching in PERL?',
                    'options': [
                        'A) ==',
                        'B) =~',
                        'C) ~~',
                        'D) !='
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The =~ operator is used for pattern matching and binding in PERL.'
                },
                {
                    'question': 'What does the /g flag do in a substitution?',
                    'options': [
                        'A) Makes it case-insensitive',
                        'B) Makes it global (replace all occurrences)',
                        'C) Makes it greedy',
                        'D) Makes it generate a list'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The /g flag makes substitution global, replacing all occurrences instead of just the first.'
                },
                {
                    'question': 'What does \\d match in a PERL regular expression?',
                    'options': [
                        'A) Any character',
                        'B) A digit (0-9)',
                        'C) A letter',
                        'D) Whitespace'
                    ],
                    'correct_answer': 'B',
                    'explanation': '\\d is a character class that matches any digit from 0 to 9.'
                },
                {
                    'question': 'How do you make a pattern match case-insensitive?',
                    'options': [
                        'A) Use /c flag',
                        'B) Use /i flag',
                        'C) Use /I flag',
                        'D) Use /case flag'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'The /i flag makes pattern matching case-insensitive.'
                },
                {
                    'question': 'What do parentheses () do in a regular expression?',
                    'options': [
                        'A) Create character classes',
                        'B) Create capture groups',
                        'C) Create anchors',
                        'D) Create quantifiers'
                    ],
                    'correct_answer': 'B',
                    'explanation': 'Parentheses create capture groups that can be referenced later as $1, $2, etc.'
                }
            ]
        }
    }

def get_quiz_by_criteria(language, topic, difficulty='mixed', count=5):
    """Get quiz questions based on criteria"""
    
    quiz_data = get_sample_quiz_questions()
    
    # Get questions for the specified language and topic
    if language not in quiz_data:
        return []
    
    if topic.lower() not in quiz_data[language]:
        # If specific topic not found, get from all topics
        all_questions = []
        for topic_questions in quiz_data[language].values():
            all_questions.extend(topic_questions)
        questions = all_questions
    else:
        questions = quiz_data[language][topic.lower()]
    
    # Return requested number of questions (or all if fewer available)
    import random
    if len(questions) <= count:
        return questions
    else:
        return random.sample(questions, count)

def get_topics_by_language(language):
    """Get available topics for a language"""
    
    quiz_data = get_sample_quiz_questions()
    
    if language not in quiz_data:
        return []
    
    return list(quiz_data[language].keys())

def validate_quiz_answer(question, user_answer):
    """Validate if user answer is correct"""
    
    correct_answer = question.get('correct_answer', '')
    
    # Extract just the letter if user_answer includes the full option text
    if len(user_answer) > 1:
        user_answer = user_answer[0].upper()
    else:
        user_answer = user_answer.upper()
    
    return user_answer == correct_answer

def get_quiz_statistics(questions, user_answers):
    """Calculate quiz statistics"""
    
    if not questions or not user_answers:
        return {
            'total_questions': 0,
            'correct_answers': 0,
            'score_percentage': 0,
            'passed': False
        }
    
    correct_count = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        if i < len(user_answers):
            if validate_quiz_answer(question, user_answers[i]):
                correct_count += 1
    
    score_percentage = (correct_count / total_questions) * 100
    passed = score_percentage >= 70  # 70% passing grade
    
    return {
        'total_questions': total_questions,
        'correct_answers': correct_count,
        'score_percentage': score_percentage,
        'passed': passed
    }
