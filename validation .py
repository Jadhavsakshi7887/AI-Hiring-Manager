"""Data validation utilities for candidate information"""

import re
import validators
from typing import Dict, List, Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address format"""
    if not email:
        return False, "Email is required"
    
    if not validators.email(email):
        return False, "Please enter a valid email address"
    
    return True, ""

def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number format"""
    if not phone:
        return False, "Phone number is required"
    
    # Remove all non-digit characters
    cleaned_phone = re.sub(r'\D', '', phone)
    
    if len(cleaned_phone) < 10:
        return False, "Phone number must be at least 10 digits"
    
    if len(cleaned_phone) > 15:
        return False, "Phone number is too long"
    
    return True, ""

def validate_name(name: str) -> Tuple[bool, str]:
    """Validate candidate name"""
    if not name or not name.strip():
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if not re.match(r'^[a-zA-Z\s\-\.\']+$', name.strip()):
        return False, "Name contains invalid characters"
    
    return True, ""

def validate_experience(experience: str) -> Tuple[bool, str]:
    """Validate years of experience"""
    if not experience:
        return False, "Years of experience is required"
    
    try:
        years = float(experience)
        if years < 0:
            return False, "Years of experience cannot be negative"
        if years > 50:
            return False, "Years of experience seems too high"
        return True, ""
    except ValueError:
        return False, "Please enter a valid number for years of experience"

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';\\]', '', str(text))
    
    # Limit length
    sanitized = sanitized[:500]
    
    return sanitized.strip()

def validate_tech_stack(tech_stack: str) -> Tuple[bool, str]:
    """Validate and parse technology stack input"""
    if not tech_stack or not tech_stack.strip():
        return False, "Please enter at least one technology"
    
    # Split by common separators and clean
    techs = [tech.strip() for tech in re.split(r'[,;|\n]', tech_stack) if tech.strip()]
    
    if len(techs) == 0:
        return False, "Please enter at least one technology"
    
    if len(techs) > 10:
        return False, "Please limit to 10 technologies maximum"
    
    return True, ""
