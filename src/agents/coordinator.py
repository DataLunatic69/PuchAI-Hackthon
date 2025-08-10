# src/agents/coordinator.py
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import BaseAgent, AgentResponse
from utils.prompts import SystemPrompts
from typing import Dict, Any

class QueryClassification(BaseModel):
    """Classification of student query for routing"""
    
    agent_type: str = Field(
        description="Agent to handle query: COMPLAINT, LOST_FOUND, MESS, RULES, STATUS, or GENERAL"
    )
    urgency: str = Field(
        description="Urgency level: low, medium, high, urgent"
    )
    has_safety_concern: str = Field(
        description="Safety concern present? Yes or No"
    )
    brief_summary: str = Field(
        description="Brief summary of the query for context"
    )

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Coordinator")
    
    def get_system_prompt(self) -> str:
        return SystemPrompts.get_coordinator_prompt()
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        # Classify the query
        classification = await self._classify_query(query)
        
        # Route to appropriate agent
        if classification.agent_type == "COMPLAINT":
            from src.agents.complaint_handler import ComplaintAgent
            agent = ComplaintAgent()
        elif classification.agent_type == "LOST_FOUND":
            from src.agents.lost_found import LostFoundAgent
            agent = LostFoundAgent()
        elif classification.agent_type == "MESS":
            from src.agents.mess_management import MessAgent
            agent = MessAgent()
        elif classification.agent_type == "RULES":
            from src.agents.rules_policy import RulesAgent
            agent = RulesAgent()
        elif classification.agent_type == "STATUS":
            from src.agents.status_updates import StatusAgent
            agent = StatusAgent()
        else:
            return AgentResponse(
                content="Hello! I'm HostelBuddy, your AI assistant for hostel matters. I can help with complaints, lost & found, mess queries, rules, and facility status. What do you need assistance with?",
                urgency="low"
            )
        
        # Add classification context
        enhanced_context = {
            **context,
            "urgency": classification.urgency,
            "safety_concern": classification.has_safety_concern == "Yes",
            "summary": classification.brief_summary
        }
        
        return await agent.process_query(query, enhanced_context)
    
    async def _classify_query(self, query: str) -> QueryClassification:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "Student query: {query}")
        ])
        
        structured_llm = self.get_structured_llm(QueryClassification)
        chain = prompt | structured_llm
        
        return await chain.ainvoke({"query": query})