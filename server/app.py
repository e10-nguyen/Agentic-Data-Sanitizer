from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class TextData(BaseModel):
    text: str

def sanitize_text(text: str) -> str:
    """Sanitize text by removing sensitive patterns"""
    sanitized = text
    
    # Remove email addresses
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', sanitized)
    
    # Remove phone numbers
    sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[REDACTED_PHONE]', sanitized)
    
    # Remove credit card numbers
    sanitized = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[REDACTED_CC]', sanitized)
    
    return sanitized

@app.post("/api/sanitize")
async def sanitize(text_data: TextData):
    """Sanitize text content"""
    try:
        sanitized_text = sanitize_text(text_data.text)
        return {"sanitizedText": sanitized_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
