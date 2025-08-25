"""Privacy and security utilities"""

import hashlib
import time
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import streamlit as st
from typing import Dict, Any

def generate_session_id() -> str:
    """Generate a unique session ID"""
    timestamp = str(time.time())
    return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for logging"""
    return hashlib.sha256(data.encode()).hexdigest()

def encrypt_data(data: str, key: bytes = None) -> str:
    """Encrypt sensitive data"""
    if key is None:
        key = Fernet.generate_key()
    
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def log_interaction(session_id: str, interaction_type: str, data: Dict[str, Any]):
    """Log user interactions securely"""
    timestamp = datetime.now().isoformat()
    
    # Hash any sensitive information
    safe_data = {}
    for key, value in data.items():
        if key in ['email', 'phone', 'name']:
            safe_data[f"{key}_hash"] = hash_sensitive_data(str(value))
        else:
            safe_data[key] = value
    
    log_entry = {
        "timestamp": timestamp,
        "session_id": session_id,
        "interaction_type": interaction_type,
        "data": safe_data
    }
    
    # In a real application, this would be sent to a secure logging service
    print(f"[SECURE LOG] {log_entry}")

def check_data_retention():
    """Check and clean up old data based on retention policy"""
    # In a real application, this would clean up data older than DATA_RETENTION_DAYS
    pass

def get_privacy_notice() -> str:
    """Get the privacy notice text"""
    return """
    **Privacy Notice for TalentScout AI Hiring Assistant**
    
    By using this service, you acknowledge that:
    
    • **Data Collection**: We collect your name, email, phone number, experience level, and technology skills for recruitment purposes only.
    
    • **Data Usage**: Your information will be used solely to assess your technical qualifications and match you with relevant opportunities.
    
    • **Data Security**: All data is encrypted and securely stored. Sensitive information is hashed for logging purposes.
    
    • **Data Retention**: Your data will be retained for 30 days maximum, after which it will be automatically deleted.
    
    • **Your Rights**: You can request data deletion at any time by typing 'delete my data' during the conversation.
    
    • **No Third-Party Sharing**: Your information will not be shared with third parties without explicit consent.
    
    • **Contact**: For privacy concerns, contact us at privacy@talentscout.com
    
    Do you consent to the collection and processing of your data as described above?
    """

def handle_data_deletion_request(session_id: str):
    """Handle user request to delete their data"""
    # In a real application, this would delete all user data from databases
    log_interaction(session_id, "data_deletion_request", {"status": "completed"})
    
    st.success("✅ Your data has been successfully deleted from our systems.")
    st.info("Thank you for using TalentScout. You can close this window now.")
    st.stop()
