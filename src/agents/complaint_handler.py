# src/agents/complaint_handler.py
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_agent import BaseAgent, AgentResponse
from config.form_links import FormLinks
from typing import Dict, Any

class ComplaintAnalysis(BaseModel):
    """Analysis of a maintenance complaint"""
    
    issue_type: str = Field(
        description="Type: electrical, plumbing, furniture, room, internet, or general"
    )
    severity: str = Field(
        description="Severity: minor, moderate, major, critical"
    )
    immediate_action_needed: str = Field(
        description="Immediate action required? Yes or No"
    )
    temporary_solution: str = Field(
        description="Any temporary solution or safety advice to give"
    )
    estimated_resolution: str = Field(
        description="Estimated time to fix: hours, 1-2 days, 3-5 days, 1+ weeks"
    )

class ComplaintAgent(BaseAgent):
    def __init__(self):
        super().__init__("Complaint Handler")
    
    def get_system_prompt(self) -> str:
        return """You are a maintenance complaint specialist for hostel management.

        Analyze complaints and categorize:
        - electrical: fans, lights, outlets, wiring, power issues
        - plumbing: taps, showers, toilets, leaks, water pressure
        - furniture: beds, chairs, tables, storage, doors, windows
        - room: cleanliness, pests, ventilation, general room issues
        - internet: WiFi, connectivity, network problems
        - general: other facility issues

        Assess severity:
        - critical: Safety hazards, major damage, urgent health concerns
        - major: Essential services not working, significant problems
        - moderate: Important but not urgent issues
        - minor: Small problems, cosmetic issues

        Always provide helpful temporary solutions and realistic timelines.
        """
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        # Analyze the complaint
        analysis = await self._analyze_complaint(query, context)
        
        # Get appropriate form
        form_link = FormLinks.get_complaint_form(analysis.issue_type)
        
        # Generate response
        response_content = await self._generate_response(query, analysis, context)
        
        # Determine urgency
        urgency = "urgent" if analysis.severity == "critical" else "high" if analysis.severity == "major" else "medium"
        
        next_steps = [
            f"Fill out the complaint form: {form_link}",
            "You'll receive a complaint ID for tracking",
            f"Expected resolution: {analysis.estimated_resolution}",
            "Contact hostel office if urgent"
        ]
        
        return AgentResponse(
            content=response_content,
            form_link=form_link,
            next_steps=next_steps,
            urgency=urgency
        )
    
    async def _analyze_complaint(self, query: str, context: Dict[str, Any]) -> ComplaintAnalysis:
        # Add image analysis if available
        image_context = ""
        if context.get("image_data"):
            image_analysis = await self.analyze_image(
                context["image_data"],
                "Analyze this hostel maintenance issue. Describe the problem and assess severity."
            )
            image_context = f"\nImage analysis: {image_analysis}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "Complaint: {query}{image_context}")
        ])
        
        structured_llm = self.get_structured_llm(ComplaintAnalysis)
        chain = prompt | structured_llm
        
        return await chain.ainvoke({"query": query, "image_context": image_context})
    
    async def _generate_response(self, query: str, analysis: ComplaintAnalysis, context: Dict[str, Any]) -> str:
        response_prompt = f"""
        I understand you're having a {analysis.issue_type} issue. {analysis.temporary_solution}
        
        This appears to be a {analysis.severity} issue that typically takes {analysis.estimated_resolution} to resolve.
        
        {"⚠️ Please take immediate safety precautions and contact the hostel office directly!" if analysis.immediate_action_needed == "Yes" else ""}
        
        To formally report this issue, please fill out the appropriate complaint form below.
        """
        
        return response_prompt.strip()