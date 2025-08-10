# src/agents/lost_found.py
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_agent import BaseAgent, AgentResponse
from src.tools.form_selector import FormSelector
from src.utils.prompts import SystemPrompts
from typing import Dict, Any

class LostFoundAnalysis(BaseModel):
    """Analysis of lost or found item query"""
    
    item_category: str = Field(
        description="Category: electronics, clothing, books, accessories, documents, keys, or other"
    )
    is_lost_item: str = Field(
        description="Is this about a LOST item? Yes or No"
    )
    is_found_item: str = Field(
        description="Is this about a FOUND item? Yes or No"
    )
    urgency_level: str = Field(
        description="Urgency: low, medium, high (high for important documents/electronics)"
    )
    suggested_search_areas: str = Field(
        description="Comma-separated list of areas to search based on item type and context"
    )

class LostFoundAgent(BaseAgent):
    def __init__(self):
        super().__init__("Lost & Found Specialist")
    
    def get_system_prompt(self) -> str:
        return SystemPrompts.get_lost_found_prompt()
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        # Analyze the lost/found query
        analysis = await self._analyze_lost_found(query, context)
        
        # Determine if it's lost or found
        if analysis.is_lost_item == "Yes":
            return await self._handle_lost_item(query, analysis, context)
        elif analysis.is_found_item == "Yes":
            return await self._handle_found_item(query, analysis, context)
        else:
            return await self._handle_general_inquiry(query, analysis)
    
    async def _analyze_lost_found(self, query: str, context: Dict[str, Any]) -> LostFoundAnalysis:
        # Add image analysis if available
        image_context = ""
        if context.get("image_data"):
            image_analysis = await self.analyze_image(
                context["image_data"],
                SystemPrompts.get_vision_analysis_prompt()
            )
            image_context = f"\nImage shows: {image_analysis}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "Query: {query}{image_context}")
        ])
        
        structured_llm = self.get_structured_llm(LostFoundAnalysis)
        chain = prompt | structured_llm
        
        return await chain.ainvoke({"query": query, "image_context": image_context})
    
    async def _handle_lost_item(self, query: str, analysis: LostFoundAnalysis, context: Dict[str, Any]) -> AgentResponse:
        search_areas = analysis.suggested_search_areas.split(", ")
        
        # Use FormSelector for consistent form handling
        form_link, form_explanation = FormSelector.get_lost_found_form(True, analysis.item_category)
        
        content = f"""I understand you've lost your {analysis.item_category}. Don't worry, let's help you find it!

**First, try checking these areas:**
{chr(10).join(f"• {area}" for area in search_areas[:4])}

**Tips for finding your item:**
- Ask friends if they've seen it
- Check with mess staff if lost during meals
- Look in the last place you remember using it
- Check lost & found box at reception

{form_explanation}"""

        next_steps = [
            "Search the suggested areas thoroughly",
            "Ask friends and roommates",
            "Fill out the lost item report form",
            "Check back in 2-3 days for updates"
        ]
        
        return AgentResponse(
            content=content,
            form_link=form_link,
            next_steps=next_steps,
            urgency=analysis.urgency_level
        )
    
    async def _handle_found_item(self, query: str, analysis: LostFoundAnalysis, context: Dict[str, Any]) -> AgentResponse:
        form_link, form_explanation = FormSelector.get_lost_found_form(False, analysis.item_category)
        
        content = f"""Thank you for being helpful to fellow students! You found a {analysis.item_category}.

                        **What to do next:**
                        - Keep the item in a safe place
                        - Don't try to unlock or access personal items
                        - Report it using the form below
                        - We'll match it with lost item reports

                        **Current safe storage options:**
                        - Your room (for small items)
                        - Hand over to reception desk
                        - Keep with you until owner is found

                        {form_explanation}"""

        next_steps = [
            "Secure the item safely",
            "Fill out the found item report form",
            "We'll contact you when we find the owner",
            "Thank you for your honesty!"
        ]
        
        return AgentResponse(
            content=content,
            form_link=form_link,
            next_steps=next_steps,
            urgency="medium"
        )
    
    async def _handle_general_inquiry(self, query: str, analysis: LostFoundAnalysis) -> AgentResponse:
        content = """I can help you with lost and found items!

                    **If you LOST something:**
                    - Tell me what you lost and where you last saw it
                    - I'll suggest places to search
                    - Help you report it officially

                    **If you FOUND something:**
                    - Describe what you found
                    - I'll guide you on how to return it
                    - Help you report it to match with owners

                    What specific item do you need help with?"""
                            
        return AgentResponse(content=content, urgency="low")