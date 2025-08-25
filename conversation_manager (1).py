"""Conversation flow management for the hiring assistant"""

import streamlit as st
from typing import Dict, List, Any, Optional
from utils.validation import *
from utils.questions import generate_questions_for_tech_stack
from utils.privacy import log_interaction, handle_data_deletion_request
from utils.llm_integration import evaluate_technical_response, enhance_conversation_response
from config import STAGES, EXIT_KEYWORDS
import re

class ConversationManager:
    def __init__(self, session_id: str):
        self.session_id = session_id
        
        # Initialize session state
        if 'stage' not in st.session_state:
            st.session_state.stage = STAGES["GREETING"]
        if 'candidate_data' not in st.session_state:
            st.session_state.candidate_data = {}
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'technical_questions' not in st.session_state:
            st.session_state.technical_questions = {}
        if 'consent_given' not in st.session_state:
            st.session_state.consent_given = False

    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        st.session_state.messages.append({"role": role, "content": content})

    def check_exit_intent(self, user_input: str) -> bool:
        """Check if user wants to exit the conversation"""
        if not user_input:
            return False
        
        user_input_lower = user_input.lower().strip()
        
        # Check for exact matches
        if user_input_lower in EXIT_KEYWORDS:
            return True
        
        # Check for partial matches
        for keyword in EXIT_KEYWORDS:
            if keyword in user_input_lower:
                return True
        
        # Check for data deletion request
        if "delete my data" in user_input_lower or "delete data" in user_input_lower:
            handle_data_deletion_request(self.session_id)
            return True
        
        return False

    def handle_greeting_stage(self) -> str:
        """Handle the initial greeting stage"""
        greeting_message = f"""
        👋 **Welcome to {st.session_state.get('company_name', 'TalentScout')} AI Hiring Assistant!**
        
        I'm here to help assess your technical skills and match you with exciting opportunities. 
        
        This conversation will take about 5-10 minutes and will cover:
        • Basic information collection
        • Your technology experience
        • A few technical questions based on your skills
        
        Before we begin, I need to inform you about our data privacy practices.
        
        **Type 'continue' to proceed to the privacy notice, or 'exit' to leave.**
        """
        
        st.session_state.stage = STAGES["CONSENT"]
        return greeting_message

    def handle_consent_stage(self, user_input: str) -> str:
        """Handle privacy consent stage"""
        if not user_input:
            return "Please type 'continue' to proceed or 'exit' to leave."
        
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['continue', 'proceed', 'next', 'yes']:
            from utils.privacy import get_privacy_notice
            privacy_notice = get_privacy_notice()
            st.session_state.stage = STAGES["INFO_COLLECTION"]
            return privacy_notice + "\n\n**Please type 'I consent' to agree and continue, or 'exit' to leave.**"
        
        return "Please type 'continue' to proceed with the privacy notice, or 'exit' to leave the conversation."

    def handle_info_collection_stage(self, user_input: str) -> str:
        """Handle candidate information collection"""
        if not st.session_state.consent_given:
            if user_input.lower().strip() in ['i consent', 'consent', 'agree', 'i agree']:
                st.session_state.consent_given = True
                log_interaction(self.session_id, "consent_given", {"timestamp": str(st.session_state.get('timestamp'))})
                return self._start_info_collection()
            else:
                return "Please type 'I consent' to agree to our privacy policy and continue, or 'exit' to leave."
        
        return self._collect_candidate_info(user_input)

    def _start_info_collection(self) -> str:
        """Start the information collection process"""
        return """
        ✅ **Thank you for your consent!**
        
        Now, let's collect some basic information about you.
        
        **Please provide your full name:**
        """

    def _collect_candidate_info(self, user_input: str) -> str:
        """Collect candidate information step by step"""
        candidate_data = st.session_state.candidate_data
        
        # Name collection
        if 'name' not in candidate_data:
            is_valid, error_msg = validate_name(user_input)
            if not is_valid:
                return f"❌ {error_msg}\n\n**Please provide your full name:**"
            
            candidate_data['name'] = sanitize_input(user_input)
            return "**Great! Now please provide your email address:**"
        
        # Email collection
        elif 'email' not in candidate_data:
            is_valid, error_msg = validate_email(user_input)
            if not is_valid:
                return f"❌ {error_msg}\n\n**Please provide your email address:**"
            
            candidate_data['email'] = sanitize_input(user_input)
            return "**Perfect! Now please provide your phone number:**"
        
        # Phone collection
        elif 'phone' not in candidate_data:
            is_valid, error_msg = validate_phone(user_input)
            if not is_valid:
                return f"❌ {error_msg}\n\n**Please provide your phone number:**"
            
            candidate_data['phone'] = sanitize_input(user_input)
            return "**Excellent! How many years of professional experience do you have? (Enter a number):**"
        
        # Experience collection
        elif 'experience' not in candidate_data:
            is_valid, error_msg = validate_experience(user_input)
            if not is_valid:
                return f"❌ {error_msg}\n\n**Please enter your years of professional experience (as a number):**"
            
            candidate_data['experience'] = float(user_input)
            st.session_state.stage = STAGES["TECH_ASSESSMENT"]
            return """
            **Fantastic! Now let's talk about your technical skills.**
            
            Please list the programming languages, frameworks, and technologies you're proficient in.
            You can separate them with commas (e.g., "Python, React, MongoDB, AWS"):
            """
        
        return "Something went wrong. Please try again."

    def handle_tech_assessment_stage(self, user_input: str) -> str:
        """Handle technology stack assessment"""
        is_valid, error_msg = validate_tech_stack(user_input)
        if not is_valid:
            return f"❌ {error_msg}\n\n**Please list your technical skills (separated by commas):**"
        
        # Parse and store tech stack
        tech_list = [tech.strip() for tech in re.split(r'[,;|\n]', user_input) if tech.strip()]
        st.session_state.candidate_data['tech_stack'] = tech_list
        
        candidate_experience = st.session_state.candidate_data.get('experience', 2.0)
        
        # Generate technical questions using LLM
        questions_by_tech = generate_questions_for_tech_stack(
            tech_list, 
            candidate_experience=candidate_experience
        )
        st.session_state.technical_questions = questions_by_tech
        
        # Log the complete candidate profile
        log_interaction(self.session_id, "candidate_profile_complete", st.session_state.candidate_data)
        
        st.session_state.stage = STAGES["TECHNICAL_QUESTIONS"]
        
        total_questions = sum(len(questions) for questions in questions_by_tech.values())
        
        return f"""
        **Excellent! I've identified your technical expertise in: {', '.join(tech_list)}**
        
        Based on your {candidate_experience} years of experience and skills, I've prepared {total_questions} personalized technical questions to better assess your knowledge.
        
        **Ready to begin the technical assessment? Type 'ready' to start:**
        """

    def handle_technical_questions_stage(self, user_input: str) -> str:
        """Handle technical questions and answers"""
        if not st.session_state.technical_questions:
            return "No technical questions available. Something went wrong."
        
        # Check if we're starting the technical questions
        if st.session_state.current_question_index == 0 and user_input.lower().strip() not in ['ready', 'start', 'begin', 'yes']:
            return "**Type 'ready' when you're prepared to start the technical questions:**"
        
        # Get all questions in a flat list
        all_questions = []
        for tech, questions in st.session_state.technical_questions.items():
            for question in questions:
                all_questions.append((tech, question))
        
        current_index = st.session_state.current_question_index
        
        # If we have a previous answer to store and evaluate
        if current_index > 0 and user_input.strip():
            prev_tech, prev_question = all_questions[current_index - 1]
            
            # Store the answer
            if 'answers' not in st.session_state.candidate_data:
                st.session_state.candidate_data['answers'] = {}
            
            st.session_state.candidate_data['answers'][f"{prev_tech}_{current_index-1}"] = {
                'question': prev_question,
                'answer': sanitize_input(user_input),
                'technology': prev_tech
            }
            
            try:
                evaluation_response = evaluate_technical_response(
                    question=prev_question,
                    answer=user_input,
                    technology=prev_tech
                )
                
                # Add the evaluation as a message
                self.add_message("assistant", evaluation_response)
                
            except Exception as e:
                # Fallback evaluation response
                evaluation_response = "Thank you for that detailed explanation. Your technical knowledge is evident in your response."
                self.add_message("assistant", evaluation_response)
        
        # Check if we've completed all questions
        if current_index >= len(all_questions):
            st.session_state.stage = STAGES["COMPLETION"]
            return self._complete_assessment()
        
        # Ask the next question
        tech, question = all_questions[current_index]
        st.session_state.current_question_index += 1
        
        progress = f"**Question {current_index + 1} of {len(all_questions)} ({tech.upper()})**"
        
        return f"""
        {progress}
        
        {question}
        
        **Please provide your answer:**
        """

    def _complete_assessment(self) -> str:
        """Complete the technical assessment"""
        candidate_data = st.session_state.candidate_data
        
        # Log the completion
        log_interaction(self.session_id, "assessment_complete", {
            "total_questions": st.session_state.current_question_index,
            "technologies_assessed": list(st.session_state.technical_questions.keys())
        })
        
        return f"""
        🎉 **Congratulations, {candidate_data.get('name', 'Candidate')}!**
        
        You've successfully completed the TalentScout AI technical assessment!
        
        **Assessment Summary:**
        • **Name:** {candidate_data.get('name', 'N/A')}
        • **Experience:** {candidate_data.get('experience', 'N/A')} years
        • **Technologies:** {', '.join(candidate_data.get('tech_stack', []))}
        • **Questions Answered:** {len(candidate_data.get('answers', {}))}
        
        **What happens next?**
        1. Our technical team will review your responses
        2. We'll match your profile with suitable opportunities
        3. You'll hear from us within 2-3 business days at {candidate_data.get('email', 'your email')}
        
        **Thank you for your time and interest in TalentScout opportunities!**
        
        You can now close this window or type 'restart' to begin a new assessment.
        """

    def process_message(self, user_input: str) -> str:
        """Process user input based on current conversation stage"""
        if not user_input:
            return "Please provide a response to continue."
        
        # Check for exit intent
        if self.check_exit_intent(user_input):
            return """
            👋 **Thank you for your interest in TalentScout!**
            
            Your session has been ended. If you'd like to complete the assessment later, 
            please start a new conversation.
            
            Have a great day!
            """
        
        # Handle restart request
        if user_input.lower().strip() == 'restart':
            # Clear session state
            for key in list(st.session_state.keys()):
                if key != 'session_id':
                    del st.session_state[key]
            
            st.session_state.stage = STAGES["GREETING"]
            st.session_state.candidate_data = {}
            st.session_state.messages = []
            st.session_state.current_question_index = 0
            st.session_state.technical_questions = {}
            st.session_state.consent_given = False
            
            return self.handle_greeting_stage()
        
        # Route to appropriate stage handler
        current_stage = st.session_state.stage
        
        if current_stage == STAGES["GREETING"]:
            return self.handle_greeting_stage()
        elif current_stage == STAGES["CONSENT"]:
            return self.handle_consent_stage(user_input)
        elif current_stage == STAGES["INFO_COLLECTION"]:
            return self.handle_info_collection_stage(user_input)
        elif current_stage == STAGES["TECH_ASSESSMENT"]:
            return self.handle_tech_assessment_stage(user_input)
        elif current_stage == STAGES["TECHNICAL_QUESTIONS"]:
            return self.handle_technical_questions_stage(user_input)
        elif current_stage == STAGES["COMPLETION"]:
            return "Assessment completed! Type 'restart' to begin a new assessment or close the window."
        else:
            return "Something went wrong. Please type 'restart' to begin again."
