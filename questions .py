"""Technical question generation based on technology stack with LLM integration"""

from typing import List, Dict
import random
from utils.llm_integration import generate_technical_questions

# Comprehensive question bank organized by technology (fallback)
FALLBACK_QUESTION_BANK = {
    # Frontend Technologies
    "react": [
        "What are React Hooks and how do they differ from class components?",
        "Explain the concept of Virtual DOM and its benefits.",
        "How do you handle state management in a large React application?",
        "What is the difference between controlled and uncontrolled components?",
        "How would you optimize the performance of a React application?"
    ],
    "angular": [
        "What is dependency injection in Angular and why is it important?",
        "Explain the difference between Angular components and directives.",
        "How do you handle routing in Angular applications?",
        "What are Angular services and how do you create them?",
        "Describe the Angular component lifecycle hooks."
    ],
    "vue": [
        "What is the Vue.js reactivity system and how does it work?",
        "Explain the difference between Vue 2 and Vue 3 Composition API.",
        "How do you handle component communication in Vue.js?",
        "What are Vue directives and can you create custom ones?",
        "How would you implement state management in a Vue application?"
    ],
    "javascript": [
        "Explain the difference between let, const, and var in JavaScript.",
        "What are closures in JavaScript and provide an example?",
        "How does prototypal inheritance work in JavaScript?",
        "What is the event loop and how does it handle asynchronous operations?",
        "Explain the concept of hoisting in JavaScript."
    ],
    "typescript": [
        "What are the main benefits of using TypeScript over JavaScript?",
        "Explain generics in TypeScript with an example.",
        "What is the difference between interface and type in TypeScript?",
        "How do you handle optional properties and null checks in TypeScript?",
        "What are decorators in TypeScript and how are they used?"
    ],
    
    # Backend Technologies
    "python": [
        "What are Python decorators and how do you create custom ones?",
        "Explain the difference between lists and tuples in Python.",
        "How does Python's garbage collection work?",
        "What is the Global Interpreter Lock (GIL) in Python?",
        "How do you handle exceptions in Python applications?"
    ],
    "java": [
        "Explain the concept of Object-Oriented Programming in Java.",
        "What is the difference between abstract classes and interfaces?",
        "How does garbage collection work in Java?",
        "What are Java Streams and how do you use them?",
        "Explain the concept of multithreading in Java."
    ],
    "node": [
        "What is the event-driven architecture in Node.js?",
        "How do you handle asynchronous operations in Node.js?",
        "What is the difference between require() and import in Node.js?",
        "How do you manage memory leaks in Node.js applications?",
        "Explain the concept of middleware in Express.js."
    ],
    "express": [
        "How do you implement authentication in Express.js?",
        "What are Express.js middleware functions and how do they work?",
        "How do you handle error handling in Express applications?",
        "What is the difference between app.use() and app.get() in Express?",
        "How do you implement rate limiting in Express.js?"
    ],
    
    # Databases
    "mongodb": [
        "What is the difference between SQL and NoSQL databases?",
        "How do you design schemas in MongoDB?",
        "What are MongoDB aggregation pipelines?",
        "How do you handle indexing in MongoDB for performance?",
        "Explain the concept of sharding in MongoDB."
    ],
    "mysql": [
        "What are the different types of JOINs in MySQL?",
        "How do you optimize MySQL queries for better performance?",
        "What is database normalization and why is it important?",
        "How do you handle transactions in MySQL?",
        "What are stored procedures and when would you use them?"
    ],
    "postgresql": [
        "What are the advantages of PostgreSQL over other databases?",
        "How do you implement full-text search in PostgreSQL?",
        "What are PostgreSQL extensions and how do you use them?",
        "How do you handle JSON data in PostgreSQL?",
        "Explain the concept of ACID properties in PostgreSQL."
    ],
    
    # Cloud & DevOps
    "aws": [
        "What are the core services of AWS and their use cases?",
        "How do you implement auto-scaling in AWS?",
        "What is the difference between EC2 and Lambda?",
        "How do you secure applications deployed on AWS?",
        "Explain the concept of Infrastructure as Code with AWS."
    ],
    "docker": [
        "What is containerization and how does Docker implement it?",
        "How do you optimize Docker images for production?",
        "What is the difference between Docker images and containers?",
        "How do you handle data persistence in Docker containers?",
        "Explain Docker networking and how containers communicate."
    ],
    "kubernetes": [
        "What are the core components of Kubernetes architecture?",
        "How do you deploy applications to Kubernetes clusters?",
        "What are Kubernetes pods and how do they work?",
        "How do you handle service discovery in Kubernetes?",
        "Explain the concept of Kubernetes namespaces."
    ]
}

def normalize_tech_name(tech: str) -> str:
    """Normalize technology name for matching"""
    tech_lower = tech.lower().strip()
    
    # Handle common variations
    tech_mapping = {
        "js": "javascript",
        "ts": "typescript",
        "nodejs": "node",
        "node.js": "node",
        "reactjs": "react",
        "react.js": "react",
        "angularjs": "angular",
        "vuejs": "vue",
        "vue.js": "vue",
        "mongo": "mongodb",
        "postgres": "postgresql",
        "k8s": "kubernetes",
        "expressjs": "express",
        "express.js": "express"
    }
    
    return tech_mapping.get(tech_lower, tech_lower)

def get_fallback_questions(tech: str, max_questions: int = 3) -> List[str]:
    """Get fallback questions from the static question bank"""
    normalized_tech = normalize_tech_name(tech)
    
    if normalized_tech in FALLBACK_QUESTION_BANK:
        available_questions = FALLBACK_QUESTION_BANK[normalized_tech]
        return random.sample(
            available_questions, 
            min(len(available_questions), max_questions)
        )
    else:
        # Generate generic questions for unknown technologies
        return [
            f"What are the key features and benefits of {tech}?",
            f"How would you implement best practices when working with {tech}?",
            f"What challenges have you faced while working with {tech} and how did you solve them?"
        ][:max_questions]

def generate_questions_for_tech_stack(tech_stack: List[str], max_questions_per_tech: int = 3, candidate_experience: float = 2.0) -> Dict[str, List[str]]:
    """Generate technical questions based on candidate's technology stack using LLM with fallback"""
    questions_by_tech = {}
    
    for tech in tech_stack:
        try:
            llm_questions = generate_technical_questions(
                technology=tech,
                experience_years=candidate_experience,
                num_questions=max_questions_per_tech
            )
            
            if llm_questions and len(llm_questions) > 0:
                questions_by_tech[tech] = llm_questions
            else:
                # Fall back to static questions if LLM fails
                questions_by_tech[tech] = get_fallback_questions(tech, max_questions_per_tech)
                
        except Exception as e:
            print(f"LLM question generation failed for {tech}: {e}")
            questions_by_tech[tech] = get_fallback_questions(tech, max_questions_per_tech)
    
    return questions_by_tech

def get_all_supported_technologies() -> List[str]:
    """Get list of all supported technologies"""
    return list(FALLBACK_QUESTION_BANK.keys())
