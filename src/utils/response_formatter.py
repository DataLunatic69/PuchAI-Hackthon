# src/utils/response_formatter.py
from typing import List, Optional
from agents.base_agent import AgentResponse

class ResponseFormatter:
    @staticmethod
    def format_agent_response(response: AgentResponse) -> str:
        """Format agent response for MCP output"""
        result = response.content
        
        # Add form link if provided
        if response.form_link:
            result += f"\n\n📝 **Complete this form to proceed:**\n{response.form_link}"
        
        # Add next steps if provided
        if response.next_steps:
            result += f"\n\n📋 **Next Steps:**"
            for i, step in enumerate(response.next_steps, 1):
                result += f"\n{i}. {step}"
        
        # Add urgency indicator
        urgency_indicators = {
            "urgent": "🚨 **URGENT**",
            "high": "⚠️ **HIGH PRIORITY**", 
            "medium": "📝 **MEDIUM PRIORITY**",
            "low": "ℹ️ **INFO**"
        }
        
        if response.urgency in urgency_indicators:
            indicator = urgency_indicators[response.urgency]
            result = f"{indicator}\n\n{result}"
        
        # Add emergency contact for urgent issues
        if response.urgency == "urgent":
            result += f"\n\n🆘 **For immediate assistance, contact hostel office directly: +91-XXXXXXXXXX**"
        
        return result
    
    @staticmethod
    def format_error_response(error_message: str) -> str:
        """Format error messages consistently"""
        return f"""❌ **Error Processing Request**

{error_message}

**What you can do:**
1. Try rephrasing your question
2. Provide more specific details
3. Contact hostel office directly: +91-XXXXXXXXXX

**Common issues:**
- Image too large (max 10MB)
- Unclear question type
- Network connectivity problems"""

    @staticmethod
    def format_greeting_response() -> str:
        """Format initial greeting message"""
        return """🏠 **Welcome to HostelBuddy!**

I'm your AI assistant for all hostel-related needs. I can help you with:

🔧 **Complaints & Repairs**
- Electrical, plumbing, furniture issues
- Room problems and maintenance requests

🔍 **Lost & Found**
- Report lost items
- Register found items

🍽️ **Mess Services**
- Today's menu and timings
- Food feedback and complaints

📋 **Rules & Policies**
- Hostel rules and procedures
- Visitor policies and curfew information

📊 **Facility Status**
- Power, water, internet status
- Maintenance schedules

**How to use:**
Just describe your issue or question in plain English. You can also upload photos for better assistance!

What can I help you with today?"""