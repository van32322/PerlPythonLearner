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
    
    def get_chatbot_response(self, user_message: str, context: str = "", language: str = "python") -> str:
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
            
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting right now. Error: {str(e)}"
    
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code and provide suggestions for improvement"""
        try:
            prompt = f"""Analyze the following {language.upper()} code and provide feedback in JSON format:

Code:
```{language}
{code}
