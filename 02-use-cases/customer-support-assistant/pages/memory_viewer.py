import streamlit as st
import json
from bedrock_agentcore.memory import MemoryClient
from scripts.utils import get_ssm_parameter
from app_modules.auth import AuthManager

st.set_page_config(
    page_title="Memory Viewer - Customer Support",
    page_icon="🧠",
    layout="wide"
)

def get_memory_strategies():
    """Get memory strategies with namespace templates"""
    return {
        "fact_extractor": {
            "name": "Factual Information",
            "namespace_template": "support/user/{actorId}/facts",
            "description": "Extracts and stores factual information"
        },
        "conversation_summary": {
            "name": "Conversation Summaries", 
            "namespace_template": "support/user/{actorId}/{sessionId}",
            "description": "Captures summaries of conversations"
        },
        "user_preferences": {
            "name": "User Preferences",
            "namespace_template": "support/user/{actorId}/preferences", 
            "description": "Captures user preferences and settings"
        }
    }

def main():
    st.title("🧠 Customer Support Memory Viewer")
    st.markdown("View stored memories from the CustomerSupportLiveAgent")
    
    # Initialize auth manager
    auth_manager = AuthManager()
    
    # Check authentication
    if not auth_manager.is_authenticated():
        st.warning("Please authenticate first by going to the main chat page.")
        st.stop()
    
    # Get user info
    user_claims = auth_manager.get_user_claims()
    actor_id = user_claims.get("cognito:username") if user_claims else "unknown"
    
    # Get memory ID from SSM
    try:
        memory_id = get_ssm_parameter("/app/customersupport/agentcore/memory_id")
        st.success(f"Memory ID: `{memory_id}`")
    except Exception as e:
        st.error(f"Failed to get memory ID: {e}")
        st.stop()
    
    # Initialize memory client
    memory_client = MemoryClient()
    
    # Display current user info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Actor ID:** {actor_id}")
    with col2:
        st.info(f"**Email:** {user_claims.get('email', 'N/A') if user_claims else 'N/A'}")
    
    st.divider()
    
    # Get memory strategies
    strategies = get_memory_strategies()
    
    # Display memory summary
    st.subheader("📚 Customer Memory Summary")
    
    # Get current session ID from Streamlit session state
    session_id = st.session_state.get("session_id", "unknown")
    st.info(f"**Current Session ID:** {session_id}")
    
    for strategy_key, strategy_info in strategies.items():
        # Replace placeholders with actual values
        namespace = strategy_info["namespace_template"].replace("{actorId}", actor_id).replace("{sessionId}", session_id)
        
        with st.expander(f"🔍 {strategy_info['name']}", expanded=True):
            st.markdown(f"**Description:** {strategy_info['description']}")
            st.markdown(f"**Namespace:** `{namespace}`")
            try:
                # Retrieve memories for this namespace
                memories = memory_client.retrieve_memories(
                    memory_id=memory_id,
                    namespace=namespace,
                    query="customer information and preferences",
                    top_k=10
                )
                
                if memories:
                    st.success(f"Found {len(memories)} memory items")
                    
                    # Display each memory
                    for i, memory in enumerate(memories, 1):
                        with st.container():
                            st.markdown(f"**Memory {i}:**")
                            
                            if isinstance(memory, dict):
                                # Extract content
                                content = memory.get('content', {})
                                if isinstance(content, dict):
                                    text = content.get('text', 'No text content')
                                    st.markdown(f"```\n{text}\n```")
                                else:
                                    st.markdown(f"```\n{str(content)}\n```")
                                
                                # Show metadata if available
                                if 'metadata' in memory:
                                    with st.expander("Metadata", expanded=False):
                                        st.json(memory['metadata'])
                            else:
                                st.markdown(f"```\n{str(memory)}\n```")
                            
                            st.divider()
                else:
                    st.info("No memories found for this namespace")
                    
            except Exception as e:
                st.error(f"Error retrieving {strategy_info['name']} memories: {e}")
    
    # Add refresh button
    if st.button("🔄 Refresh Memory Data"):
        st.rerun()

if __name__ == "__main__":
    main()