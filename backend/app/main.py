from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import openai
from loguru import logger

class ChatRequest(BaseModel):
    message: str
    api_key: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ANVE Customer Service AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Configure OpenAI with the provided API key
        openai.api_key = request.api_key
        
        # Create chat completion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful customer service AI assistant for ANVE. Be professional, friendly, and concise in your responses."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            max_tokens=500
        )
        
        # Extract the assistant's response
        ai_response = response.choices[0].message.content
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 