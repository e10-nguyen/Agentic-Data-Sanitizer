from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class TextData(BaseModel):
    text: str

def sanitize_text(text: str) -> str:
    """
    This acts as the main sanitization function.
    Here, we can call a LLM agent to respond with sanitized text.
    """
    sanitized = text
    
    # EXAMPLE: Remove phone numbers
    sanitized = re.sub(r'\d{3}[-.]?\d{4}\b', '[PHONE_NUMBER]', sanitized)

    # Do any other sanitization here... call LLM and do post processing...
    
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
