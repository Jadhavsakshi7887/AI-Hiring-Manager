# AI Hiring Manager

An intelligent Streamlit-based chatbot powered by Google Gemini for technical candidate screening and assessment.

## Features

- **AI-Powered Conversations**: Uses Google Gemini LLM for intelligent question generation and response evaluation
- **Intelligent Conversation Flow**: Guides candidates through structured information collection
- **Privacy-First Design**: GDPR compliant with data encryption and automatic deletion
- **Dynamic Technical Assessment**: Generates personalized questions based on candidate's technology stack and experience level
- **Real-time Validation**: Validates email, phone, and other inputs with helpful error messages
- **Comprehensive Question Bank**: 100+ technical questions across multiple technologies with AI enhancement
- **Secure Data Handling**: All sensitive data is hashed and encrypted
- **Session Management**: Automatic session tracking and timeout handling
- **Professional UI**: Modern chat interface with progress tracking and candidate profile sidebar

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   \`\`\`
   GEMINI_API_KEY=your_gemini_api_key_here
   \`\`\`

4. **Get Gemini API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

5. **Run the application:**
   \`\`\`bash
   streamlit run main.py
   \`\`\`

6. **Open your browser** to `http://localhost:8501`

## Project Structure

\`\`\`
ai-hiring-manager/
├── main.py                    # Main Streamlit application
├── conversation_manager.py    # Conversation flow logic with LLM integration
├── config.py                 # Configuration settings and LLM prompts
├── requirements.txt          # Python dependencies
├── utils/
│   ├── validation.py         # Input validation utilities
│   ├── questions.py          # Technical question generation with AI
│   ├── privacy.py            # Privacy and security utilities
│   └── llm_integration.py    # Google Gemini LLM integration
└── README.md                 # This file
\`\`\`

## Usage

1. **Start the application** and navigate to the provided URL
2. **Follow the AI-guided conversation flow:**
   - Privacy consent and data handling agreement
   - Personal information collection (name, email, phone, experience)
   - Technology stack assessment with experience levels
   - AI-generated technical questions personalized to your skills
   - Intelligent follow-up responses and evaluation
3. **Complete the assessment** to receive next steps information

## AI-Powered Features

- **Dynamic Question Generation**: Gemini creates personalized technical questions based on candidate experience
- **Intelligent Response Evaluation**: AI provides encouraging follow-up responses to technical answers
- **Context-Aware Conversations**: Maintains natural dialogue flow throughout the assessment
- **Fallback Mechanisms**: Graceful handling when AI services are unavailable

## Supported Technologies

The system includes AI-enhanced technical questions for:
- **Frontend**: React, Angular, Vue.js, JavaScript, TypeScript, HTML/CSS
- **Backend**: Python, Java, Node.js, Express.js, Django, Flask
- **Databases**: MongoDB, MySQL, PostgreSQL, Redis
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD
- **Mobile**: React Native, Flutter, iOS, Android
- **Data Science**: Machine Learning, Data Analysis, AI/ML frameworks

## Privacy & Security

- All data is encrypted and securely handled
- Sensitive information is hashed for logging
- Automatic data deletion after 30 days
- Users can request immediate data deletion
- GDPR compliant privacy notices and consent mechanisms
- No data shared with third parties without explicit consent

## Customization

- **Add new technologies**: Update `QUESTION_BANK` in `utils/questions.py`
- **Modify AI prompts**: Edit `SYSTEM_PROMPTS` in `config.py`
- **Update conversation flow**: Edit `conversation_manager.py`
- **Change styling**: Modify CSS in `main.py`
- **Adjust privacy settings**: Update privacy configurations in `config.py`

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Google Generative AI 0.3.2+
- Valid Gemini API key
- See `requirements.txt` for full dependency list

## Troubleshooting

**API Key Issues:**
- Ensure your Gemini API key is correctly set in the `.env` file
- Verify the API key has proper permissions

**Installation Problems:**
- Use Python 3.8 or higher
- Consider using a virtual environment: `python -m venv venv`

**Performance:**
- The app includes fallback mechanisms when AI services are slow or unavailable
- Questions will still be generated from the static question bank if needed

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the AI Hiring Manager.
