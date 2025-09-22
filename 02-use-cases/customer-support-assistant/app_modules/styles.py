import streamlit as st


def apply_custom_styles():
    """Apply modern CSS styles to the Streamlit app"""
    st.markdown(
        """
        <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Hide Streamlit branding but keep functionality */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-1rs6os {visibility: hidden;}
        .css-17ziqus {visibility: hidden;}
        
        /* Modern sidebar */
        .css-1d391kg, .css-1lcbmhc, .css-1cypcdb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        .css-1d391kg .stMarkdown, .css-1lcbmhc .stMarkdown {
            color: white !important;
        }
        
        /* Sidebar button styling */
        .css-1d391kg .stButton > button, .css-1lcbmhc .stButton > button {
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 20px !important;
        }
        
        .css-1d391kg .stButton > button:hover, .css-1lcbmhc .stButton > button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
        }
        
        /* Chat bubbles */
        .user-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 18px;
            border-radius: 20px 20px 4px 20px;
            margin: 8px 0;
            display: inline-block;
            max-width: 85%;
            word-wrap: break-word;
            box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);
            font-weight: 500;
        }
        
        .assistant-bubble {
            background: #ffffff;
            color: #2d3748;
            padding: 12px 18px;
            border-radius: 20px 20px 20px 4px;
            margin: 8px 0;
            display: inline-block;
            max-width: 85%;
            word-wrap: break-word;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
        }
        
        .thinking-bubble {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #2d3748;
            padding: 12px 18px;
            border-radius: 20px;
            margin: 8px 0;
            display: inline-block;
            max-width: 85%;
            word-wrap: break-word;
            font-style: italic;
            animation: pulse 2s infinite;
        }
        
        /* Animations */
        @keyframes pulse {
            0% { opacity: 0.8; }
            50% { opacity: 1; }
            100% { opacity: 0.8; }
        }
        
        .typing-cursor::after {
            content: '▋';
            animation: blink 1s infinite;
            color: #667eea;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        /* Modern header */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 0 0 20px 20px;
            margin: -1rem -1rem 2rem -1rem;
            text-align: center;
            color: white;
        }
        
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .main-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-top: 0.5rem;
            font-weight: 300;
        }
        
        /* Chat input styling */
        .stChatInput {
            border-radius: 25px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .stChatInput:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Sidebar improvements */
        .sidebar-section {
            background: rgba(255, 255, 255, 0.1) !important;
            padding: 1rem !important;
            border-radius: 10px !important;
            margin: 1rem 0 !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .sidebar-title {
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            color: white !important;
        }
        
        /* Force sidebar visibility */
        .css-1d391kg, .css-1lcbmhc {
            visibility: visible !important;
            display: block !important;
        }
        
        /* Code blocks */
        .stCode {
            background: #1a202c;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Chat container */
        .chat-container {
            background: #f8fafc;
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )