# Dockerfile for HostelBuddy MCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY pyproject.toml ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY config/ ./config/
COPY forms/ ./forms/

# Create non-root user
RUN useradd -m -u 1000 hostelbuddy && \
    chown -R hostelbuddy:hostelbuddy /app
USER hostelbuddy

# Expose port
EXPOSE 8086

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f -H "Authorization: Bearer ${AUTH_TOKEN}" http://localhost:8086/mcp/ || exit 1

# Start command
CMD ["python", "src/mcp_server.py"]