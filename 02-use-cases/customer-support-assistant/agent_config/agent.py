from .utils import get_ssm_parameter
from agent_config.memory_hook_provider import MemoryHook
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands_tools import current_time, retrieve
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from strands_tools.browser import AgentCoreBrowser
from typing import List


class CustomerSupport:
    def __init__(
        self,
        bearer_token: str,
        memory_hook: MemoryHook,
        bedrock_model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        system_prompt: str = None,
        tools: List[callable] = None,
    ):
        self.model_id = bedrock_model_id
        self.model = BedrockModel(
            model_id=self.model_id,
        )
        self.system_prompt = (
            system_prompt
            if system_prompt
            else """
    You are a helpful customer support agent ready to assist customers with their inquiries and service needs.
    You have access to tools to: check warrant status, view customer profiles, retrieve Knowledgebase, and browse websites to help customers.
    
    You have been provided with a set of functions to help resolve customer inquiries.
    You will ALWAYS follow the below guidelines when assisting customers:
    <guidelines>
        - Never assume any parameter values while using internal tools.
        - If you do not have the necessary information to process a request, politely ask the customer for the required details
        - You can use web browsing capabilities to help customers find product information, pricing, or other relevant details
        - Always maintain a professional and helpful tone when assisting customers
        - Focus on resolving the customer's inquiries efficiently and accurately
    </guidelines>
    """
        )

        gateway_url = get_ssm_parameter("/app/customersupport/agentcore/gateway_url")
        print(f"Gateway Endpoint - MCP URL: {gateway_url}")

        try:
            # Initialize Gateway MCP Client
            self.gateway_client = MCPClient(
                lambda: streamablehttp_client(
                    gateway_url,
                    headers={"Authorization": f"Bearer {bearer_token}"},
                )
            )
            self.gateway_client.start()
            
            # Initialize AgentCore Browser (with proper Playwright setup)
            self.agent_core_browser = AgentCoreBrowser(region="us-west-2")
            print(f"DEBUG - AgentCoreBrowser initialized: {self.agent_core_browser}")
            print(f"DEBUG - Browser tool object: {self.agent_core_browser.browser}")
            
        except Exception as e:
            raise Exception(f"Error initializing agent: {str(e)}")

        # Get tools from gateway MCP client
        gateway_tools = self.gateway_client.list_tools_sync()
        
        self.tools = (
            [
                retrieve,
                current_time,
                self.agent_core_browser.browser,
            ]
            + gateway_tools
            + (tools if tools else [])
        )
        
        print(f"DEBUG - Total tools loaded: {len(self.tools)}")
        for i, tool in enumerate(self.tools):
            print(f"DEBUG - Tool {i}: {getattr(tool, '__name__', str(tool))}")
        print(f"DEBUG - Browser tool: {self.agent_core_browser.browser}")

        self.memory_hook = memory_hook

        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            tools=self.tools,
            # hooks=[self.memory_hook],
        )

    def invoke(self, user_query: str):
        try:
            response = str(self.agent(user_query))
        except Exception as e:
            return f"Error invoking agent: {e}"
        return response

    async def stream(self, user_query: str):
        try:
            async for event in self.agent.stream_async(user_query):
                if "data" in event:
                    # Only stream text chunks to the client
                    yield event["data"]

        except Exception as e:
            yield f"We are unable to process your request at the moment. Error: {e}"
