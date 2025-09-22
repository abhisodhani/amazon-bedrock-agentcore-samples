#!/usr/bin/env python3
import sys
import os
import time
import boto3
import json
from boto3.session import Session
from bedrock_agentcore_starter_toolkit import Runtime

# Use existing Cognito configuration from SSM parameters
def get_existing_cognito_config():
    """Get existing Cognito configuration from SSM parameters"""
    ssm_client = boto3.client('ssm')
    
    try:
        discovery_url = ssm_client.get_parameter(
            Name='/app/customersupport/agentcore/cognito_discovery_url'
        )['Parameter']['Value']
        
        client_id = ssm_client.get_parameter(
            Name='/app/customersupport/agentcore/web_client_id'
        )['Parameter']['Value']
        
        return {
            'discovery_url': discovery_url,
            'client_id': client_id
        }
    except Exception as e:
        print(f"❌ Error getting Cognito config: {e}")
        sys.exit(1)

def deploy_playwright_mcp():
    print("🚀 Deploying Playwright MCP to AgentCore Runtime...")
    
    boto_session = Session()
    region = boto_session.region_name
    
    # Get existing Cognito configuration
    print("🔐 Getting existing Cognito configuration...")
    cognito_config = get_existing_cognito_config()
    
    # Configure AgentCore Runtime
    print("⚙️ Configuring AgentCore Runtime...")
    agentcore_runtime = Runtime()
    
    auth_config = {
        "customJWTAuthorizer": {
            "allowedClients": [cognito_config['client_id']],
            "discoveryUrl": cognito_config['discovery_url'],
        }
    }
    
    agentcore_runtime.configure(
        entrypoint="playwright_mcp_server.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="playwright_requirements.txt",
        region=region,
        authorizer_configuration=auth_config,
        protocol="MCP",
        agent_name="playwright_mcp_agentcore"
    )
    
    # Launch
    print("🚀 Launching to AgentCore Runtime...")
    launch_result = agentcore_runtime.launch()
    
    # Wait for ready
    print("⏳ Waiting for deployment...")
    while True:
        status = agentcore_runtime.status().endpoint['status']
        if status == 'READY':
            break
        elif status in ['CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']:
            print(f"❌ Deployment failed: {status}")
            return None
        time.sleep(10)
    
    # Store configuration
    print("💾 Storing configuration...")
    ssm_client = boto3.client('ssm', region_name=region)
    secrets_client = boto3.client('secretsmanager', region_name=region)
    
    # Store credentials
    try:
        secrets_client.create_secret(
            Name='playwright_mcp/cognito/credentials',
            SecretString=json.dumps(cognito_config)
        )
    except secrets_client.exceptions.ResourceExistsException:
        secrets_client.update_secret(
            SecretId='playwright_mcp/cognito/credentials',
            SecretString=json.dumps(cognito_config)
        )
    
    # Store Agent ARN
    ssm_client.put_parameter(
        Name='/app/customersupport/playwright/agent_arn',
        Value=launch_result.agent_arn,
        Type='String',
        Overwrite=True
    )
    
    # Store MCP URL
    encoded_arn = launch_result.agent_arn.replace(':', '%3A').replace('/', '%2F')
    mcp_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
    
    ssm_client.put_parameter(
        Name='/app/customersupport/playwright/mcp_url',
        Value=mcp_url,
        Type='String',
        Overwrite=True
    )
    
    print("✅ Deployment completed!")
    print(f"Agent ARN: {launch_result.agent_arn}")
    print(f"MCP URL: {mcp_url}")
    
    return launch_result.agent_arn

if __name__ == "__main__":
    deploy_playwright_mcp()