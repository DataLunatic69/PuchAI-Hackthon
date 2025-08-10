# src/mcp_server.py
import asyncio
from typing import Annotated, Optional
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp.server.auth.provider import AccessToken
from mcp import ErrorData, McpError
from mcp.types import INTERNAL_ERROR
from pydantic import Field
from agents.coordinator import CoordinatorAgent
from utils.response_formatter import ResponseFormatter
from utils.validators import QueryValidator

load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(token=token, client_id="puch-client", scopes=["*"], expires_at=None)
        return None

mcp = FastMCP("HostelBuddy Multi-Agent System", auth=SimpleBearerAuthProvider(TOKEN))
coordinator = CoordinatorAgent()

@mcp.tool
async def validate() -> str:
    """Validate tool required by Puch AI"""
    return MY_NUMBER

@mcp.tool
async def hostel_assistant(
    query: Annotated[str, Field(description="Student's hostel-related question or issue")],
    image_data: Annotated[Optional[str], Field(description="Base64 image (optional)")] = None
) -> str:
    """
    AI-powered hostel assistant with specialized agents for complaints, lost & found, 
    mess queries, rules, and status updates. Supports image analysis for better assistance.
    """
    try:
        # Validate query
        query_validation = QueryValidator.validate_query(query)
        if not query_validation["is_valid"]:
            return ResponseFormatter.format_error_response(
                f"Query validation failed: {', '.join(query_validation['warnings'])}"
            )
        
        # Validate image if provided
        if image_data:
            image_validation = QueryValidator.validate_image_data(image_data)
            if not image_validation["is_valid"]:
                return ResponseFormatter.format_error_response(
                    f"Image validation failed: {', '.join(image_validation['warnings'])}"
                )
        
        # Process query through coordinator agent
        context = {"image_data": image_data} if image_data else {}
        response = await coordinator.process_query(query_validation["sanitized_query"], context)
        
        # Format response using ResponseFormatter
        return ResponseFormatter.format_agent_response(response)
        
    except Exception as e:
        raise McpError(ErrorData(
            code=INTERNAL_ERROR, 
            message=f"Error processing hostel query: {str(e)}"
        ))

@mcp.tool
async def hostel_help() -> str:
    """Get help and information about HostelBuddy capabilities"""
    return ResponseFormatter.format_greeting_response()

async def main():
    print("🏠 Starting HostelBuddy MCP server on http://0.0.0.0:8086")
    print("📋 Available tools: hostel_assistant, hostel_help, validate")
    print("🤖 Agents loaded: Coordinator, Complaint Handler, Lost & Found, Mess Manager, Rules Advisor, Status Monitor")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())