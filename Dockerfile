FROM python:3.10-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY playwright_requirements.txt .
RUN pip install --no-cache-dir -r playwright_requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application code
COPY playwright_mcp_server.py .

# Expose port
EXPOSE 8931

# Run the MCP server
CMD ["python", "playwright_mcp_server.py"]