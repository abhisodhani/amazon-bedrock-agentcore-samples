import sys
import streamlit as st
from .auth import AuthManager
from .chat import ChatManager
from .styles import apply_custom_styles


def main():
    """Main application entry point"""
    # Parse command line arguments
    agent_name = "default"
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg.startswith("--agent="):
                agent_name = arg.split("=")[1]

    # Configure page
    st.set_page_config(
        page_title="Customer Support Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom styles
    apply_custom_styles()

    # Initialize managers
    auth_manager = AuthManager()
    chat_manager = ChatManager(agent_name)

    # Handle OAuth callback
    auth_manager.handle_oauth_callback()

    # Check authentication status
    if auth_manager.is_authenticated():
        # Authenticated user interface
        render_authenticated_interface(auth_manager, chat_manager)
    else:
        # Login interface
        render_login_interface(auth_manager)


def render_authenticated_interface(
    auth_manager: AuthManager, chat_manager: ChatManager
):
    """Render the interface for authenticated users"""
    # Modern sidebar
    st.sidebar.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-title">🔑 Access Tokens</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.code(auth_manager.cookies.get("tokens"))

    # Logout button with better styling
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", key="logout_btn", help="Sign out of the application"):
        auth_manager.logout()

    st.sidebar.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-title">🤖 Agent Details</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.code(st.session_state["agent_arn"])

    st.sidebar.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-title">🎯 Session ID</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.code(st.session_state["session_id"])

    # Modern header
    st.markdown(
        """
        <div class="main-header">
            <h1 class="main-title">🤖 Customer Support Assistant</h1>
            <p class="main-subtitle">Powered by Amazon Bedrock AgentCore • Get instant help with warranties, troubleshooting & more</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Get user info and tokens
    tokens = auth_manager.get_tokens()
    user_claims = auth_manager.get_user_claims()
    
    # Debug logging
    print(f"DEBUG - Tokens: {tokens}")
    print(f"DEBUG - User claims: {user_claims}")
    print(f"DEBUG - Agent ARN: {st.session_state.get('agent_arn')}")
    print(f"DEBUG - Session ID: {st.session_state.get('session_id')}")
    print(f"DEBUG - Client ID from auth: {auth_manager.client_id}")

    # Initialize conversation if needed
    if not st.session_state.get("messages"):
        chat_manager.initialize_default_conversation(
            user_claims, tokens["access_token"]
        )
    else:
        # Display chat history
        chat_manager.display_chat_history()

    # Modern chat input
    st.markdown(
        """
        <div style="margin-top: 2rem;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    if prompt := st.chat_input("✨ Ask me about warranties, troubleshooting, or schedule a meeting..."):
        chat_manager.process_user_message(prompt, user_claims, tokens["access_token"])


def render_login_interface(auth_manager: AuthManager):
    """Render the login interface"""
    login_url = auth_manager.get_login_url()
    st.markdown(
        f'<meta http-equiv="refresh" content="0;url={login_url}">',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
