#!/usr/bin/env python3
import subprocess
import sys
import time

def run_command(cmd, description):
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ {description} failed")
        return False
    print(f"✅ {description} completed")
    return True

def main():
    print("🔧 Installing Playwright and testing MCP server")
    
    # Install dependencies
    if not run_command("pip install -r playwright_requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright browsers"):
        return False
    
    # Start MCP server in background
    print("\n🚀 Starting Playwright MCP server...")
    server_process = subprocess.Popen([sys.executable, "playwright_mcp_server.py"])
    time.sleep(5)  # Wait for server to start
    
    try:
        # Test local server
        if not run_command("python test_playwright_local.py", "Testing local MCP server"):
            return False
        
        print("\n✅ Local tests passed! Ready for deployment.")
        
    finally:
        # Clean up
        server_process.terminate()
        server_process.wait()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Next step: Run 'python deploy_playwright.py' to deploy to AgentCore Runtime")
    exit(0 if success else 1)