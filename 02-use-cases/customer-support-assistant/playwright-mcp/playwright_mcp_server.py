from mcp.server.fastmcp import FastMCP
import asyncio
from playwright.async_api import async_playwright

mcp = FastMCP(host="0.0.0.0", port=8931, stateless_http=True)

@mcp.tool()
async def navigate_to_url(url: str) -> str:
    """Navigate to a URL and return page title"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(url)
        title = await page.title()
        return f"Navigated to {url}. Title: {title}"
    finally:
        await browser.close()
        await playwright.stop()

@mcp.tool()
async def get_page_content(url: str, selector: str = None) -> str:
    """Get page content or specific element text"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(url)
        if selector:
            element = await page.query_selector(selector)
            content = await element.text_content() if element else "Element not found"
        else:
            content = await page.text_content('body')
        return content[:500] + "..." if len(content) > 500 else content
    finally:
        await browser.close()
        await playwright.stop()

@mcp.tool()
async def click_element(url: str, selector: str) -> str:
    """Click element and return result"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(url)
        await page.click(selector)
        return f"Clicked element: {selector}"
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")