import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('streamlit_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add this to your chat.py invoke_endpoint method
def debug_invoke_endpoint(self, agent_arn, payload, session_id, bearer_token, endpoint_name="DEFAULT"):
    logging.info(f"Invoking endpoint with agent_arn: {agent_arn}")
    logging.info(f"Session ID: {session_id}")
    logging.info(f"Payload: {payload}")
    
    try:
        # Your existing invoke_endpoint code here
        pass
    except Exception as e:
        logging.error(f"Error in invoke_endpoint: {str(e)}")
        logging.error(f"Exception type: {type(e)}")
        raise