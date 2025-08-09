# src/tools/vision_analyzer.py
from src.tools.groq_client import get_vision_llm
from langchain_core.messages import HumanMessage

async def analyze_image(image_base64: str, prompt: str) -> str:
    """Analyze image using Groq vision model"""
    try:
        llm = get_vision_llm()
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                }
            ]
        )
        
        response = await llm.ainvoke([message])
        return response.content
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"