import subprocess
import tempfile
import os
import sys
from typing import Dict, Tuple
import streamlit as st

class SafeCodeExecutor:
    """Safe code execution environment with limited capabilities"""
    
    def __init__(self):
        self.timeout = 10  # Maximum execution time in seconds
        self.max_output_length = 2000  # Maximum output length
    
    def execute_python(self, code: str) -> Dict:
        """Execute Python code safely"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute the code with timeout
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tempfile.gettempdir()
                )
                
                output = result.stdout
                error = result.stderr
                
                # Limit output length
                if len(output) > self.max_output_length:
                    output = output[:self.max_output_length] + "\n... (output truncated)"
                
                if len(error) > self.max_output_length:
                    error = error[:self.max_output_length] + "\n... (error truncated)"
                
                return {
                    'success': result.returncode == 0,
                    'output': output,
                    'error': error,
                    'execution_time': 'N/A'  # Would need more complex timing
                }
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': f'Code execution timed out after {self.timeout} seconds',
                'execution_time': f'>{self.timeout}s'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Execution error: {str(e)}',
                'execution_time': 'N/A'
            }
    
    def execute_perl(self, code: str) -> Dict:
        """Execute PERL code safely"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute the code with timeout
                result = subprocess.run(
                    ['perl', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tempfile.gettempdir()
                )
                
                output = result.stdout
                error = result.stderr
                
                # Limit output length
                if len(output) > self.max_output_length:
                    output = output[:self.max_output_length] + "\n... (output truncated)"
                
                if len(error) > self.max_output_length:
                    error = error[:self.max_output_length] + "\n... (error truncated)"
                
                return {
                    'success': result.returncode == 0,
                    'output': output,
                    'error': error,
                    'execution_time': 'N/A'
                }
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': f'Code execution timed out after {self.timeout} seconds',
                'execution_time': f'>{self.timeout}s'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': 'PERL interpreter not found. Please ensure PERL is installed.',
                'execution_time': 'N/A'
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Execution error: {str(e)}',
                'execution_time': 'N/A'
            }
    
    def execute_code(self, code: str, language: str) -> Dict:
        """Execute code based on language"""
        if language.lower() == 'python':
            return self.execute_python(code)
        elif language.lower() == 'perl':
            return self.execute_perl(code)
        else:
            return {
                'success': False,
                'output': '',
                'error': f'Unsupported language: {language}',
                'execution_time': 'N/A'
            }
    
    def validate_code_safety(self, code: str, language: str) -> Tuple[bool, str]:
        """Basic code safety validation"""
        dangerous_patterns = {
            'python': [
                'import os', '__import__', 'exec(', 'eval(',
                'open(', 'file(', 'input(', 'raw_input(',
                'subprocess', 'system', 'popen'
            ],
            'perl': [
                'system(', 'exec(', '`', 'open(',
                'unlink', 'rmdir', 'mkdir'
            ]
        }
        
        patterns = dangerous_patterns.get(language.lower(), [])
        
        for pattern in patterns:
            if pattern in code:
                return False, f"Potentially unsafe code detected: {pattern}"
        
        return True, "Code appears safe"

# Global code executor instance
code_executor = SafeCodeExecutor()
