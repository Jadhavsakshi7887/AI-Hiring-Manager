"""Configuration settings for TalentScout AI Hiring Assistant"""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-pro"

APP_TITLE = "TalentScout AI Hiring Assistant"
COMPANY_NAME = "TalentScout"
MAX_QUESTIONS_PER_TECH = 3
SESSION_TIMEOUT = 3600  

DATA_RETENTION_DAYS = 30
REQUIRE_CONSENT = True

STAGES = {
    "GREETING": "greeting",
    "CONSENT": "consent", 
    "INFO_COLLECTION": "info_collection",
    "TECH_ASSESSMENT": "tech_assessment",
    "TECHNICAL_QUESTIONS": "technical_questions",
    "COMPLETION": "completion"
}

EXIT_KEYWORDS = [
    "exit", "quit", "bye", "goodbye", "stop", "end", "finish", 
    "no thanks", "not interested", "cancel"
]

SYSTEM_PROMPTS = {
    "TECHNICAL_QUESTION_GENERATOR": """You are an expert technical interviewer for a hiring company called TalentScout. 
    Generate {num_questions} relevant, practical technical questions for a candidate with experience in {technology}.
    
    Questions should be:
    - Appropriate for {experience_level} level ({years} years experience)
    - Focused on real-world application, not just theory
    - Clear and specific
    - Progressively challenging
    
    Return only the questions, numbered 1-{num_questions}, without additional commentary.""",
    
    "RESPONSE_EVALUATOR": """You are an expert technical interviewer evaluating a candidate's response.
    
    Question: {question}
    Technology: {technology}
    Candidate's Answer: {answer}
    
    Provide a brief, encouraging follow-up response (2-3 sentences) that:
    - Acknowledges their answer professionally
    - Shows you understand their response
    - Maintains a positive, supportive tone
    - Does NOT reveal if the answer is correct or incorrect
    
    Keep it conversational and encouraging.""",
    
    "CONVERSATION_ENHANCER": """You are a friendly, professional AI hiring assistant for TalentScout.
    
    Context: {context}
    User Input: {user_input}
    Current Stage: {stage}
    
    Generate a natural, helpful response that:
    - Maintains professional but friendly tone
    - Guides the conversation forward appropriately
    - Shows understanding of the hiring context
    - Keeps responses concise (2-3 sentences max)
    
    Do not ask technical questions - that's handled separately."""
}
