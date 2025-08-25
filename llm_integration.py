"""LLM integration utilities using Google Gemini"""

import google.generativeai as genai
import streamlit as st
from typing import List, Dict, Any, Optional
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPTS
import time
import random

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = None
        if GEMINI_API_KEY:
            try:
                self.model = genai.GenerativeModel(GEMINI_MODEL)
            except Exception as e:
                st.error(f"Failed to initialize Gemini: {e}")
    
    def generate_response(self, prompt: str, max_retries: int = 3) -> str:
        """Generate response using Gemini with retry logic"""
        if not self.model:
            return self._fallback_response(prompt)
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return response.text.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    st.warning(f"LLM unavailable, using fallback response")
                    return self._fallback_response(prompt)
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when LLM is unavailable"""
        if "technical question" in prompt.lower():
            return self._fallback_technical_questions()
        elif "evaluate" in prompt.lower() or "response" in prompt.lower():
            return self._fallback_evaluation()
        else:
            return "Thank you for your response. Let's continue with the next step."
    
    def _fallback_technical_questions(self) -> str:
        """Fallback technical questions when LLM is unavailable"""
        fallback_questions = [
            "1. Describe a challenging project you've worked on and how you approached solving the technical problems.",
            "2. How do you ensure code quality and maintainability in your projects?",
            "3. Explain a time when you had to learn a new technology quickly. How did you approach it?"
        ]
        return "\n".join(fallback_questions)
    
    def _fallback_evaluation(self) -> str:
        """Fallback evaluation responses"""
        responses = [
            "Thank you for that detailed explanation. Your experience shows good technical understanding.",
            "I appreciate your thorough response. That demonstrates solid problem-solving skills.",
            "Great answer! Your approach shows good technical thinking and practical experience."
        ]
        return random.choice(responses)

# Global client instance
gemini_client = GeminiClient()

def generate_technical_questions(technology: str, experience_years: float, num_questions: int = 3) -> List[str]:
    """Generate technical questions using Gemini"""
    experience_level = "junior" if experience_years < 2 else "mid-level" if experience_years < 5 else "senior"
    
    prompt = SYSTEM_PROMPTS["TECHNICAL_QUESTION_GENERATOR"].format(
        num_questions=num_questions,
        technology=technology,
        experience_level=experience_level,
        years=experience_years
    )
    
    response = gemini_client.generate_response(prompt)
    
    # Parse the response into individual questions
    questions = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            # Remove numbering and clean up
            question = line.split('.', 1)[-1].strip() if '.' in line else line
            question = question.lstrip('-•').strip()
            if question:
                questions.append(question)
    
    # Ensure we have the requested number of questions
    if len(questions) < num_questions:
        # Add fallback questions if needed
        fallback = [
            f"What are the key features and benefits of {technology}?",
            f"Describe a project where you used {technology} effectively.",
            f"What challenges have you faced when working with {technology}?"
        ]
        questions.extend(fallback[:num_questions - len(questions)])
    
    return questions[:num_questions]

def evaluate_technical_response(question: str, answer: str, technology: str) -> str:
    """Generate an encouraging follow-up response using Gemini"""
    prompt = SYSTEM_PROMPTS["RESPONSE_EVALUATOR"].format(
        question=question,
        technology=technology,
        answer=answer
    )
    
    return gemini_client.generate_response(prompt)

def enhance_conversation_response(context: str, user_input: str, stage: str) -> str:
    """Enhance conversation responses using Gemini"""
    prompt = SYSTEM_PROMPTS["CONVERSATION_ENHANCER"].format(
        context=context,
        user_input=user_input,
        stage=stage
    )
    
    return gemini_client.generate_response(prompt)
