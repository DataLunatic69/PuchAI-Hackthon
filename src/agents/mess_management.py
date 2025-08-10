# src/agents/mess_management.py
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_agent import BaseAgent, AgentResponse
from src.tools.form_selector import FormSelector
from config.hostel_data import MessData
from src.utils.prompts import SystemPrompts
from typing import Dict, Any

class MessQueryAnalysis(BaseModel):
    """Analysis of mess-related query"""
    
    query_type: str = Field(
        description="Type: menu_inquiry, timing_question, feedback, complaint, dietary_request, or general"
    )
    meal_type: str = Field(
        description="Meal: breakfast, lunch, dinner, snacks, or all"
    )
    concern_level: str = Field(
        description="Concern level: info_request, minor_issue, major_complaint, health_concern"
    )
    requires_immediate_attention: str = Field(
        description="Needs immediate attention? Yes or No"
    )

class MessAgent(BaseAgent):
    def __init__(self):
        super().__init__("Mess Manager")
    
    def get_system_prompt(self) -> str:
        return SystemPrompts.get_mess_management_prompt()
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        # Analyze the mess query
        analysis = await self._analyze_mess_query(query, context)
        
        # Route based on query type
        if analysis.query_type == "menu_inquiry":
            return await self._handle_menu_inquiry(analysis)
        elif analysis.query_type == "timing_question":
            return await self._handle_timing_question(analysis)
        elif analysis.query_type == "complaint":
            return await self._handle_complaint(query, analysis, context)
        elif analysis.query_type == "feedback":
            return await self._handle_feedback(query, analysis)
        elif analysis.query_type == "dietary_request":
            return await self._handle_dietary_request(query, analysis)
        else:
            return await self._handle_general_inquiry()
    
    async def _analyze_mess_query(self, query: str, context: Dict[str, Any]) -> MessQueryAnalysis:
        # Add image analysis for food quality issues
        image_context = ""
        if context.get("image_data"):
            image_analysis = await self.analyze_image(
                context["image_data"],
                SystemPrompts.get_vision_analysis_prompt()
            )
            image_context = f"\nImage shows: {image_analysis}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "Mess query: {query}{image_context}")
        ])
        
        structured_llm = self.get_structured_llm(MessQueryAnalysis)
        chain = prompt | structured_llm
        
        return await chain.ainvoke({"query": query, "image_context": image_context})
    
    async def _handle_menu_inquiry(self, analysis: MessQueryAnalysis) -> AgentResponse:
        menu_info = MessData.get_menu_info(analysis.meal_type)
        
        content = f"""**Today's Menu Information:**

{menu_info}

**Mess Timings:**
- Breakfast: 7:00 AM - 9:00 AM
- Lunch: 12:00 PM - 2:00 PM  
- Dinner: 7:00 PM - 9:00 PM

**Weekly Menu:**
A full weekly menu is posted on the mess notice board. Special meals are served on festivals and weekends!"""
        
        return AgentResponse(content=content, urgency="low")
    
    async def _handle_timing_question(self, analysis: MessQueryAnalysis) -> AgentResponse:
        content = """**Mess Timings & Schedule:**

**Regular Timings:**
- Breakfast: 7:00 AM - 9:00 AM
- Lunch: 12:00 PM - 2:00 PM
- Dinner: 7:00 PM - 9:00 PM

**Special Timings:**
- Sundays: Extended breakfast until 10:00 AM
- Holidays: Check notice board for updates
- Late dining: Available until 9:30 PM (limited menu)

**Emergency Meals:**
Contact mess manager for special circumstances or medical needs."""
        
        return AgentResponse(content=content, urgency="low")
    
    async def _handle_complaint(self, query: str, analysis: MessQueryAnalysis, context: Dict[str, Any]) -> AgentResponse:
        urgency = "urgent" if analysis.requires_immediate_attention == "Yes" else "high" if analysis.concern_level == "health_concern" else "medium"
        
        form_link, form_explanation = FormSelector.get_mess_form("complaint", analysis.concern_level)
        
        content = f"""I understand your concern about the mess service. {"This sounds like it needs immediate attention." if analysis.requires_immediate_attention == "Yes" else "Your feedback is important for improving our services."}

**Immediate steps:**
{"• Contact mess manager immediately for health/safety issues" if analysis.concern_level == "health_concern" else "• Your complaint will be reviewed within 24 hours"}
- Fill out the complaint form for official documentation
- You'll receive a response within 2-3 working days

**For urgent food safety issues, also contact:**
- Mess Manager: [Phone number]
- Hostel Office: [Phone number]

{form_explanation}"""

        next_steps = [
            "Fill out the mess complaint form",
            "Save any evidence (photos, receipts)",
            "Follow up in 3 days if no response",
            "Contact hostel office for urgent issues"
        ]
        
        return AgentResponse(
            content=content,
            form_link=form_link,
            next_steps=next_steps,
            urgency=urgency
        )
    
    async def _handle_feedback(self, query: str, analysis: MessQueryAnalysis) -> AgentResponse:
        form_link, form_explanation = FormSelector.get_mess_form("feedback")
        
        content = f"""Thank you for wanting to share feedback about our mess services!

**Your feedback helps us:**
- Improve food quality and variety
- Better understand student preferences  
- Plan special meals and events
- Address service improvements

**Types of feedback welcome:**
- Meal suggestions and requests
- Service quality comments
- Cleanliness observations
- Positive experiences to encourage staff

{form_explanation}"""
        
        return AgentResponse(
            content=content,
            form_link=form_link,
            urgency="low"
        )
    
    async def _handle_dietary_request(self, query: str, analysis: MessQueryAnalysis) -> AgentResponse:
        form_link, form_explanation = FormSelector.get_mess_form("feedback")  # Using feedback form for dietary requests
        
        content = f"""We want to accommodate your dietary needs!

**Special diets we can help with:**
- Vegetarian/Vegan options
- Religious dietary restrictions (Halal, Jain, etc.)
- Medical dietary needs (diabetic, low-sodium, etc.)
- Food allergies and intolerances

**How it works:**
- Submit your dietary request form
- Include medical certificates if required
- Mess team will review and respond within 5 days
- Special arrangements will be documented

**Current options available:**
- Vegetarian meals at every service
- Jain food available on request
- Basic diabetic-friendly options

{form_explanation}"""
        
        next_steps = [
            "Fill out dietary request form with details",
            "Attach medical documentation if needed",
            "Meet with mess manager for discussion",
            "Follow up in 5-7 days for approval"
        ]
        
        return AgentResponse(
            content=content,
            form_link=form_link,
            next_steps=next_steps,
            urgency="medium"
        )
    
    async def _handle_general_inquiry(self) -> AgentResponse:
        content = """I'm here to help with all mess-related queries!

**I can help you with:**
- Today's menu and meal timings
- Weekly menu information  
- Food quality feedback and complaints
- Special dietary requirements
- Mess policies and procedures
- Contact information for mess staff

**Popular questions:**
- "What's for lunch today?"
- "Can I get food after mess hours?"
- "How do I request special diet meals?"
- "Who do I contact for food complaints?"

What specific information do you need about the mess?"""
        
        return AgentResponse(content=content, urgency="low")