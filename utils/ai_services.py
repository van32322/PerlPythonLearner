import json
import os
from typing import Dict, List, Optional
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
client = OpenAI(api_key=OPENAI_API_KEY)

class AILearningAssistant:
    """AI-powered learning assistant for PERL and Python"""
    
    def __init__(self):
        self.client = client
    
    def get_chatbot_response(self, user_message: str, context: str = "", language: str = "python"):
        """Get response from AI chatbot for learning support"""
        try:
            system_prompt = f"""You are an expert programming tutor specializing in {language.upper()} and PERL. 
            You help students learn programming concepts, debug code, and provide clear explanations.
            
            Guidelines:
            - Provide clear, beginner-friendly explanations
            - Use examples when explaining concepts
            - Be encouraging and supportive
            - If code is provided, analyze it and provide constructive feedback
            - Suggest best practices and common patterns
            
            Context: {context}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content or "No response received"
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "429" in error_msg:
                return "I'm temporarily unavailable due to high usage. You can still use the code practice, courses, and quiz features with sample content. Please try the AI chat again later."
            elif "api" in error_msg:
                return "I'm having connection issues right now. All other features of the learning platform are still available. Please try again in a few moments."
            else:
                return f"I'm experiencing technical difficulties. Error details: {str(e)}"
    
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code and provide suggestions for improvement"""
        try:
            prompt = f"""Analyze the following {language.upper()} code and provide feedback in JSON format:

Code:
```{language}
{code}
```

Please provide analysis in this JSON format:
{{
    "code_quality_score": (number from 1-10),
    "syntax_errors": ["list of syntax errors"],
    "logic_issues": ["list of potential logic problems"],
    "improvements": ["list of suggested improvements"],
    "best_practices": ["list of best practice recommendations"],
    "overall_feedback": "brief overall assessment"
}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are an expert {language.upper()} code reviewer. Provide detailed analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.3
            )
            
            import json
            content = response.choices[0].message.content or "{}"
            feedback = json.loads(content)
            return feedback
            
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "429" in error_msg:
                return self._get_fallback_analysis(code, language, "quota_exceeded")
            elif "api" in error_msg:
                return self._get_fallback_analysis(code, language, "api_error")
            else:
                return self._get_fallback_analysis(code, language, "general_error")
    
    def _get_fallback_analysis(self, code: str, language: str, error_type: str) -> Dict:
        """Provide basic code analysis when AI service is unavailable"""
        
        lines = code.strip().split('\n')
        has_functions = any('def ' in line for line in lines)
        has_comments = any('#' in line for line in lines)
        has_imports = any('import ' in line or 'from ' in line for line in lines)
        
        syntax_errors = []
        logic_issues = []
        improvements = []
        
        # Basic syntax checking for Python
        if language.lower() == "python":
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.count('(') != stripped.count(')'):
                    syntax_errors.append(f"Line {i}: Check parentheses balance")
                if stripped.count('[') != stripped.count(']'):
                    syntax_errors.append(f"Line {i}: Check bracket balance")
        
        # Generate improvements based on code structure
        if not has_functions and len(lines) > 10:
            improvements.append("Consider organizing code into functions")
        if not has_comments and len(lines) > 5:
            improvements.append("Add comments to explain your logic")
        if not has_imports and language.lower() == "python" and len(lines) > 3:
            improvements.append("Consider using appropriate libraries")
        
        if error_type == "quota_exceeded":
            feedback = "AI analysis temporarily unavailable due to service limits. Basic automated review provided."
        elif error_type == "api_error":
            feedback = "AI analysis service unavailable. Basic code review completed."
        else:
            feedback = "AI analysis unavailable. Automated code structure review provided."
        
        return {
            "code_quality_score": 7 if not syntax_errors else 5,
            "syntax_errors": syntax_errors if syntax_errors else ["No obvious syntax errors found"],
            "logic_issues": logic_issues if logic_issues else ["No obvious logic issues detected"],
            "improvements": improvements if improvements else ["Code structure looks good"],
            "best_practices": [
                "Use descriptive variable names",
                "Follow consistent indentation",
                "Add error handling where appropriate",
                "Test code with different inputs"
            ],
            "overall_feedback": feedback
        }
    
    def generate_quiz_questions(self, topic: str, language: str, difficulty: str = "beginner", count: int = 5) -> List[Dict]:
        """Generate quiz questions for given topic and language"""
        try:
            prompt = f"""Generate {count} multiple choice quiz questions about {topic} in {language.upper()} programming.
            
Difficulty level: {difficulty}
Format each question as JSON with this structure:
{{
    "question": "question text",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct_answer": "A",
    "explanation": "explanation of correct answer"
}}

Return an array of {count} questions in valid JSON format."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are an expert {language.upper()} programming instructor. Generate educational quiz questions in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1500,
                temperature=0.7
            )
            
            import json
            content = response.choices[0].message.content or "[]"
            result = json.loads(content)
            
            # Handle different response formats
            if isinstance(result, dict):
                if 'questions' in result:
                    return result['questions']
                elif 'quiz' in result:
                    return result['quiz']
                else:
                    # Try to find the questions in the response
                    for key, value in result.items():
                        if isinstance(value, list) and len(value) > 0:
                            return value
            elif isinstance(result, list):
                return result
            
            return []
            
        except Exception as e:
            # Return fallback quiz questions from sample data
            from data.quizzes.sample_quizzes import get_quiz_by_criteria
            return get_quiz_by_criteria(language, topic, difficulty, count)
    
    def get_learning_recommendations(self, user_progress: Dict, current_topic: str = "") -> List[str]:
        """Get personalized learning recommendations"""
        try:
            prompt = f"""Based on this learning progress data: {user_progress}
            Current topic: {current_topic}
            
            Provide 5 personalized learning recommendations to help improve programming skills.
            Focus on areas that need improvement and suggest next steps.
            
            Return as JSON array of recommendation strings."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a programming education expert. Provide specific, actionable learning recommendations."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.6
            )
            
            import json
            content = response.choices[0].message.content or "{}"
            result = json.loads(content)
            
            # Extract recommendations from various possible formats
            if isinstance(result, dict):
                if 'recommendations' in result:
                    return result['recommendations']
                elif 'suggestions' in result:
                    return result['suggestions']
                else:
                    # Try to find a list in the response
                    for value in result.values():
                        if isinstance(value, list):
                            return value
            elif isinstance(result, list):
                return result
            
            return ["Continue practicing with code examples", "Review fundamental concepts", "Take more quizzes to test understanding"]
            
        except Exception as e:
            return [
                "Practice coding exercises regularly",
                "Review course materials for better understanding",
                "Try implementing small projects",
                "Join programming communities for help",
                "Take quizzes to test your knowledge"
            ]
    
    def get_search_suggestions(self, query: str, language: str) -> List[str]:
        """Get search suggestions based on query"""
        try:
            prompt = f"""For the search query "{query}" in {language} programming, suggest 5 related search terms that would help find relevant learning content.
            
            Return as JSON array of suggestion strings."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a programming education search assistant. Suggest helpful related search terms."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=400,
                temperature=0.5
            )
            
            import json
            content = response.choices[0].message.content or "{}"
            result = json.loads(content)
            
            # Extract suggestions from response
            if isinstance(result, dict):
                for value in result.values():
                    if isinstance(value, list):
                        return value
            elif isinstance(result, list):
                return result
            
            return []
            
        except Exception as e:
            return []
    
    def explain_concept(self, concept: str, language: str):
        """Explain a programming concept"""
        try:
            prompt = f"Explain the {language} programming concept: {concept}. Keep it concise and educational."
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} programming tutor. Provide clear, concise explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.4
            )
            
            return response.choices[0].message.content or "Unable to explain concept at this time."
            
        except Exception as e:
            return f"Unable to explain {concept} at this time. Please try again later."

# Global AI assistant instance
ai_assistant = AILearningAssistant()
