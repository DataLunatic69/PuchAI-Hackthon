# src/tools/groq_client.py
import os
from langchain_groq import ChatGroq

def get_groq_llm(model: str = "openai/gpt-oss-20b", temperature: float = 0.3):
    """Get Groq LLM instance"""
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model,
        temperature=temperature
    )

def get_vision_llm():
    """Get Groq vision model"""
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.2
    )