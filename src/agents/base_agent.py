# src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, TypeVar, Type
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from tools.groq_client import get_groq_llm

T = TypeVar('T', bound=BaseModel)

class AgentResponse(BaseModel):
    content: str
    form_link: Optional[str] = None
    next_steps: Optional[List[str]] = None
    urgency: str = Field(default="medium")
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.llm = get_groq_llm()
    
    def get_structured_llm(self, response_model: Type[T]):
        """Get LLM with structured output"""
        return self.llm.with_structured_output(response_model)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    @abstractmethod
    async def process_query(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        pass
    
    async def analyze_image(self, image_base64: str, prompt: str) -> str:
        """Analyze image with vision model"""
        from src.tools.vision_analyzer import analyze_image
        return await analyze_image(image_base64, prompt)