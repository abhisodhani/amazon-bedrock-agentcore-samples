#!/usr/bin/env python3
import subprocess
import sys
import time

def run_command(cmd, description):
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ {description} failed:")
        print(result.stderr)
        return False
    print(f"✅ {description} completed")
    return True

def main():
    print("🧪 Testing and Deploying Playwright MCP Server")
    
    # Install dependencies
    if not run_command("pip install -r playwright_requirements.txt", "Installing dependencies"):
        return False
    
    if not run_command("playwright install chromium", "Installing Playwright browser"):
        return False
    
    # Start MCP server in background
    print("\n🚀 Starting Playwright MCP server...")
    server_process = subprocess.Popen([sys.executable, "playwright_mcp_server.py"])
    time.sleep(3)  # Wait for server to start
    
    try:
        # Test local server
        if not run_command("python test_playwright_local.py", "Testing local MCP server"):
            return False
        
        print("\n✅ Local tests passed! Proceeding with deployment...")
        
        # Deploy to AgentCore Runtime
        if not run_command("python deploy_playwright.py", "Deploying to AgentCore Runtime"):
            return False
        
        print("\n🎉 Deployment completed successfully!")
        print("Playwright MCP tools are now available in your Strands agent.")
        
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)