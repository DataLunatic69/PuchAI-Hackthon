# src/mcp_server.py
import asyncio
from typing import Annotated, Optional
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp.server.auth.provider import AccessToken
from pydantic import Field
from src.agents.coordinator import CoordinatorAgent

load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(token=token, client_id="puch-client", scopes=["*"], expires_at=None)
        return None

mcp = FastMCP("HostelBuddy", auth=SimpleBearerAuthProvider(TOKEN))
coordinator = CoordinatorAgent()

@mcp.tool
async def validate() -> str:
    return MY_NUMBER

@mcp.tool
async def hostel_assistant(
    query: Annotated[str, Field(description="Student's hostel-related question or issue")],
    image_data: Annotated[Optional[str], Field(description="Base64 image (optional)")] = None
) -> str:
    context = {"image_data": image_data} if image_data else {}
    response = await coordinator.process_query(query, context)
    
    result = response.content
    if response.form_link:
        result += f"\n\n📝 **Form**: {response.form_link}"
    if response.next_steps:
        result += f"\n\n**Next Steps:**\n" + "\n".join(f"• {step}" for step in response.next_steps)
    
    return result

async def main():
    print("🏠 HostelBuddy MCP Server starting on port 8086...")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())