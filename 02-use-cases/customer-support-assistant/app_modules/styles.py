import streamlit as st
import base64
from pathlib import Path

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def apply_custom_styles():
    """Apply modern CSS styles to the Streamlit app"""
    
    # Try to load the background image
    image_path = "/Users/sodhani/Documents/repo/amazon-bedrock-agentcore-samples/02-use-cases/customer-support-assistant/pages/Homepage-Banner-1-3.jpg"
    img_base64 = get_base64_image(image_path)
    
    # Build background CSS
    background_css = ""
    if img_base64:
        background_css = f"""
        .stApp {{
            background-image: url('data:image/jpg;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
        }}
        
        /* Add overlay for better readability */
        .stApp::after {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.3);
            pointer-events: none;
            z-index: -1;
        }}
        
        /* Position main content as tiny chat widget */
        .main {{
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            width: 250px !important;
            max-width: 250px !important;
            max-height: 350px !important;
            z-index: 1000 !important;
        }}
        
        .main > div {{
            background: rgba(255, 255, 255, 0.98) !important;
            border-radius: 10px !important;
            padding: 0.3rem !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            max-height: 330px !important;
            overflow-y: auto !important;
            font-size: 0.75rem !important;
        }}
        
        /* Make all content much smaller */
        .main * {{
            font-size: 0.75rem !important;
            line-height: 1.2 !important;
        }}
        
        /* Tiny chat messages */
        .main [data-testid="stChatMessage"] {{
            padding: 0.2rem !important;
            margin: 0.1rem 0 !important;
        }}
        
        /* Tiny input */
        .main .stChatInput {{
            font-size: 0.7rem !important;
            padding: 0.3rem !important;
        }}
        """
    else:
        # Fallback gradient if image not found
        background_css = """
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        """
    
    st.markdown(
        f"""
        <style>
        /* Cache buster v2.0 */
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* FORCE TINY CHAT WIDGET */
        .main {{
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            width: 200px !important;
            max-width: 200px !important;
            max-height: 300px !important;
            z-index: 9999 !important;
        }}
        
        .main > div {{
            background: rgba(255, 255, 255, 0.98) !important;
            border-radius: 8px !important;
            padding: 0.2rem !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            max-height: 280px !important;
            overflow-y: auto !important;
            font-size: 0.7rem !important;
        }}
        
        .main * {{
            font-size: 0.7rem !important;
            line-height: 1.1 !important;
        }}
        
        /* Global styles with background */
        {background_css}
        
        .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Hide Streamlit branding but keep functionality */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .css-1rs6os {{visibility: hidden;}}
        .css-17ziqus {{visibility: hidden;}}
        
        /* Modern sidebar with transparency */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        /* Chat bubbles */
        .user-bubble {{
            background: linear-gradient(135deg, #20b2aa 0%, #008b8b 100%);
            color: white;
            padding: 12px 18px;
            border-radius: 20px 20px 4px 20px;
            margin: 8px 0;
            display: inline-block;
            max-width: 85%;
            word-wrap: break-word;
            box-shadow: 0 2px 12px rgba(32, 178, 170, 0.4);
            font-weight: 500;
        }}
        
        .assistant-bubble {{
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
        }}
        
        .thinking-bubble {{
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
        }}
        
        /* Animations */
        @keyframes pulse {{
            0% {{ opacity: 0.8; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.8; }}
        }}
        
        .typing-cursor::after {{
            content: '▋';
            animation: blink 1s infinite;
            color: #667eea;
        }}
        
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        
        /* Tiny header for chat widget */
        .main-header {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
            padding: 0.3rem;
            border-radius: 6px 6px 0 0;
            margin: -0.3rem -0.3rem 0.3rem -0.3rem;
            text-align: center;
            color: white;
            backdrop-filter: blur(10px);
        }}
        
        .main-title {{
            font-size: 0.8rem;
            font-weight: 600;
            margin: 0;
        }}
        
        .main-subtitle {{
            font-size: 0.6rem;
            opacity: 0.9;
            margin-top: 0.1rem;
            font-weight: 300;
        }}
        
        /* Chat input styling with teal background */
        .stChatInput {{
            border-radius: 25px;
            border: 2px solid #20b2aa;
            transition: all 0.3s ease;
            background: rgba(32, 178, 170, 0.9) !important;
            color: white !important;
        }}
        
        .stChatInput:focus {{
            border-color: #008b8b;
            box-shadow: 0 0 0 3px rgba(32, 178, 170, 0.3);
            background: rgba(0, 139, 139, 0.95) !important;
        }}
        
        .stChatInput input {{
            background: transparent !important;
            color: white !important;
        }}
        
        .stChatInput input::placeholder {{
            color: rgba(255, 255, 255, 0.8) !important;
        }}
        
        /* Chat messages container */
        [data-testid="stChatMessageContainer"] {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(5px);
        }}
        
        /* User messages with teal background */
        [data-testid="stChatMessage"][data-testid*="user"] {{
            background: linear-gradient(135deg, #20b2aa 0%, #008b8b 100%) !important;
            color: white !important;
            border-radius: 20px 20px 4px 20px !important;
            box-shadow: 0 2px 12px rgba(32, 178, 170, 0.4) !important;
        }}
        
        /* User message content */
        [data-testid="stChatMessage"][data-testid*="user"] .stMarkdown {{
            color: white !important;
        }}
        
        /* Alternative selector for user messages */
        .stChatMessage:has([data-testid="user"]) {{
            background: linear-gradient(135deg, #20b2aa 0%, #008b8b 100%) !important;
            color: white !important;
        }}
        
        /* Sidebar improvements */
        .sidebar-section {{
            background: rgba(255, 255, 255, 0.1) !important;
            padding: 1rem !important;
            border-radius: 10px !important;
            margin: 1rem 0 !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        .sidebar-title {{
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            color: white !important;
        }}
        
        /* Code blocks */
        .stCode {{
            background: rgba(26, 32, 44, 0.95);
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        /* Chat container */
        .chat-container {{
            background: rgba(248, 250, 252, 0.95);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(5px);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )