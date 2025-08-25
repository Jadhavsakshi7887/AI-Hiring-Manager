"""
TalentScout AI Hiring Assistant
A Streamlit-based intelligent chatbot for technical candidate screening
"""

import streamlit as st
import time
from datetime import datetime
from conversation_manager import ConversationManager
from utils.privacy import generate_session_id, log_interaction
from config import APP_TITLE, COMPANY_NAME

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #f1f1f1;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
    
    .candidate-info {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .progress-indicator {
        background-color: #fff3cd;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_session_id()
        st.session_state.start_time = datetime.now()
        log_interaction(st.session_state.session_id, "session_start", {
            "timestamp": st.session_state.start_time.isoformat()
        })

def display_header():
    """Display the application header"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🤖 {APP_TITLE}</h1>
        <p>Intelligent Technical Candidate Screening</p>
    </div>
    """, unsafe_allow_html=True)

def display_progress_indicator(conversation_manager):
    """Display current progress in the conversation"""
    stage = st.session_state.get('stage', 'greeting')
    
    stage_info = {
        'greeting': ('🚀 Getting Started', 1, 6),
        'consent': ('📋 Privacy Consent', 2, 6),
        'info_collection': ('👤 Personal Information', 3, 6),
        'tech_assessment': ('💻 Technical Skills', 4, 6),
        'technical_questions': ('❓ Technical Questions', 5, 6),
        'completion': ('✅ Assessment Complete', 6, 6)
    }
    
    if stage in stage_info:
        stage_name, current, total = stage_info[stage]
        progress_percent = (current / total) * 100
        
        st.markdown(f"""
        <div class="progress-indicator">
            <strong>{stage_name}</strong> - Step {current} of {total}
            <div style="background-color: #e0e0e0; border-radius: 10px; margin-top: 0.5rem;">
                <div style="background-color: #28a745; height: 20px; border-radius: 10px; width: {progress_percent}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_candidate_info():
    """Display collected candidate information in sidebar"""
    if 'candidate_data' in st.session_state and st.session_state.candidate_data:
        candidate_data = st.session_state.candidate_data
        
        with st.sidebar:
            st.markdown("### 👤 Candidate Profile")
            
            if 'name' in candidate_data:
                st.write(f"**Name:** {candidate_data['name']}")
            
            if 'email' in candidate_data:
                st.write(f"**Email:** {candidate_data['email']}")
            
            if 'phone' in candidate_data:
                st.write(f"**Phone:** {candidate_data['phone']}")
            
            if 'experience' in candidate_data:
                st.write(f"**Experience:** {candidate_data['experience']} years")
            
            if 'tech_stack' in candidate_data:
                st.write("**Technologies:**")
                for tech in candidate_data['tech_stack']:
                    st.write(f"• {tech}")
            
            if 'answers' in candidate_data:
                st.write(f"**Questions Answered:** {len(candidate_data['answers'])}")

def display_chat_interface(conversation_manager):
    """Display the main chat interface"""
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display conversation history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    user_input = st.text_input(
        "Your response:",
        key="user_input",
        placeholder="Type your message here...",
        help="Type 'exit' at any time to end the conversation"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        send_button = st.button("Send", type="primary")
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Process user input
    if send_button and user_input:
        # Add user message to history
        conversation_manager.add_message("user", user_input)
        
        # Process the message and get response
        response = conversation_manager.process_message(user_input)
        
        # Add assistant response to history
        conversation_manager.add_message("assistant", response)
        
        # Clear input and rerun
        st.session_state.user_input = ""
        st.rerun()
    
    # Auto-start conversation if no messages
    if not st.session_state.messages:
        initial_response = conversation_manager.process_message("")
        conversation_manager.add_message("assistant", initial_response)
        st.rerun()

def display_footer():
    """Display application footer"""
    st.markdown("""
    <div class="footer">
        <p>🔒 Your privacy is protected. All data is encrypted and will be deleted after 30 days.</p>
        <p>© 2024 TalentScout AI. Built with Streamlit and Python.</p>
        <p><em>Type 'delete my data' at any time to remove your information from our systems.</em></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session
    initialize_session()
    
    # Create conversation manager
    conversation_manager = ConversationManager(st.session_state.session_id)
    
    # Display UI components
    display_header()
    display_progress_indicator(conversation_manager)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        display_chat_interface(conversation_manager)
    
    with col2:
        display_candidate_info()
    
    # Footer
    display_footer()
    
    # Session timeout check (optional)
    if 'start_time' in st.session_state:
        elapsed_time = (datetime.now() - st.session_state.start_time).total_seconds()
        if elapsed_time > 3600:  # 1 hour timeout
            st.warning("⏰ Session timeout. Please refresh the page to start a new session.")

if __name__ == "__main__":
    main()
