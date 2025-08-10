# src/utils/validators.py
import re
from typing import Dict, Any, Optional

class QueryValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def validate_query(query: str) -> Dict[str, Any]:
        """Validate user query and return validation results"""
        result = {
            "is_valid": True,
            "sanitized_query": query.strip(),
            "warnings": [],
            "length": len(query.strip())
        }
        
        # Check minimum length
        if len(query.strip()) < 3:
            result["is_valid"] = False
            result["warnings"].append("Query too short - please provide more details")
        
        # Check maximum length  
        if len(query.strip()) > 1000:
            result["is_valid"] = False
            result["warnings"].append("Query too long - please be more concise")
        
        # Check for inappropriate content (basic filter)
        inappropriate_patterns = [
            r'\b(spam|test|hello)\b',  # Common test words
            r'^[^a-zA-Z]*$'  # Only numbers/symbols
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, query.lower()):
                result["warnings"].append("Please provide a genuine hostel-related query")
        
        # Sanitize query
        result["sanitized_query"] = re.sub(r'[<>\"\'&]', '', query.strip())
        
        return result
    
    @staticmethod
    def validate_image_data(image_data: Optional[str]) -> Dict[str, Any]:
        """Validate base64 image data"""
        if not image_data:
            return {"is_valid": True, "warnings": []}
        
        result = {
            "is_valid": True,
            "warnings": [],
            "estimated_size_mb": 0
        }
        
        try:
            # Estimate size (base64 is ~33% larger than original)
            estimated_size = len(image_data) * 0.75 / (1024 * 1024)
            result["estimated_size_mb"] = round(estimated_size, 2)
            
            # Check size limits
            if estimated_size > 10:  # 10MB limit
                result["is_valid"] = False
                result["warnings"].append("Image too large - please use image under 10MB")
            
            # Basic base64 validation
            if not re.match(r'^[A-Za-z0-9+/]*={0,2}$', image_data):
                result["is_valid"] = False
                result["warnings"].append("Invalid image format")
                
        except Exception as e:
            result["is_valid"] = False
            result["warnings"].append(f"Error processing image: {str(e)}")
        
        return result
    
    @staticmethod
    def extract_urgency_keywords(query: str) -> str:
        """Extract urgency level from query text"""
        urgent_keywords = ["emergency", "urgent", "immediately", "asap", "critical", "danger"]
        high_keywords = ["broken", "not working", "damaged", "leaking", "problem", "issue"]
        medium_keywords = ["help", "question", "how", "when", "what"]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in urgent_keywords):
            return "urgent"
        elif any(keyword in query_lower for keyword in high_keywords):
            return "high"
        elif any(keyword in query_lower for keyword in medium_keywords):
            return "medium"
        else:
            return "low"