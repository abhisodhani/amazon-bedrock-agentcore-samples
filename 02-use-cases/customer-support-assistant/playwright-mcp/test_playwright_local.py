import asyncio
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def test_playwright_mcp():
    mcp_url = "http://localhost:8931/mcp"
    
    try:
        async with streamablehttp_client(mcp_url, {}, timeout=timedelta(seconds=30)) as (
            read_stream, write_stream, _
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # List tools
                tools = await session.list_tools()
                print(f"✓ Found {len(tools.tools)} tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test navigation
                print("\n🧪 Testing navigate_to_url...")
                result = await session.call_tool(
                    name="navigate_to_url",
                    arguments={"url": "https://example.com"}
                )
                print(f"✓ {result.content[0].text}")
                
                # Test content extraction
                print("\n🧪 Testing get_page_content...")
                result = await session.call_tool(
                    name="get_page_content",
                    arguments={"url": "https://example.com"}
                )
                print(f"✓ Content: {result.content[0].text[:100]}...")
                
                print("\n✅ All tests passed!")
                return True
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_playwright_mcp())
    exit(0 if success else 1)