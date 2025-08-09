# src/tools/groq_client.py
import os
from langchain_groq import ChatGroq

def get_groq_llm(model: str = "llama-3.1-70b-versatile", temperature: float = 0.3):
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
        model_name="llama-3.2-11b-vision-preview",
        temperature=0.2
    )