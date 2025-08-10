# tests/test_agents.py
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.agents.coordinator import CoordinatorAgent
from src.utils.response_formatter import ResponseFormatter

load_dotenv()

async def test_agent_responses():
    """Test different types of queries with the coordinator"""
    coordinator = CoordinatorAgent()
    
    test_cases = [
        # Complaint scenarios
        ("My room fan is not working and it's very hot", None),
        ("There's water leaking from the bathroom ceiling", None),
        ("The WiFi in Block A is very slow", None),
        
        # Lost & found scenarios  
        ("I lost my phone in the mess hall yesterday", None),
        ("I found someone's wallet near the main gate", None),
        
        # Mess queries
        ("What's today's lunch menu?", None),
        ("The food quality has been very poor lately", None),
        
        # Rules queries
        ("Can my parents stay overnight in my room?", None),
        ("What time does the hostel gate close?", None),
        
        # Status queries
        ("Is there a power cut in Block B?", None),
        ("When is the next scheduled maintenance?", None),
        
        # General queries
        ("Hello, what can you help me with?", None)
    ]
    
    print("🧪 Testing HostelBuddy Agent Responses")
    print("=" * 60)
    
    for i, (query, image_data) in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {query}")
        print("-" * 40)
        
        try:
            context = {"image_data": image_data} if image_data else {}
            response = await coordinator.process_query(query, context)
            
            # Format response
            formatted_response = ResponseFormatter.format_agent_response(response)
            
            print(f"✅ Agent Response:")
            print(formatted_response[:300] + "..." if len(formatted_response) > 300 else formatted_response)
            print(f"\n📊 Metadata:")
            print(f"   • Urgency: {response.urgency}")
            print(f"   • Confidence: {response.confidence}")
            print(f"   • Form Link: {'Yes' if response.form_link else 'No'}")
            print(f"   • Next Steps: {len(response.next_steps) if response.next_steps else 0} steps")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()

async def test_individual_agents():
    """Test individual agents directly"""
    print("\n🎯 Testing Individual Agents")
    print("=" * 40)
    
    # Test Complaint Handler
    try:
        from src.agents.complaint_handler import ComplaintAgent
        complaint_agent = ComplaintAgent()
        response = await complaint_agent.process_query("My room fan is broken", {})
        print(f"✅ Complaint Agent: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Complaint Agent Error: {e}")
    
    # Test Lost & Found
    try:
        from src.agents.lost_found import LostFoundAgent
        lost_found_agent = LostFoundAgent()
        response = await lost_found_agent.process_query("I lost my wallet", {})
        print(f"✅ Lost & Found Agent: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Lost & Found Agent Error: {e}")
    
    # Test Mess Management
    try:
        from src.agents.mess_management import MessAgent
        mess_agent = MessAgent()
        response = await mess_agent.process_query("What's for lunch today?", {})
        print(f"✅ Mess Agent: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Mess Agent Error: {e}")

if __name__ == "__main__":
    # Check environment
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set up your .env file with GROQ_API_KEY")
        exit(1)
    
    asyncio.run(test_agent_responses())
    asyncio.run(test_individual_agents())