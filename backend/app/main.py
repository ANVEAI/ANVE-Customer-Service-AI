from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import time
from datetime import datetime
import os

from app.analytics.engine import AnalyticsEngine
from app.services.ai_service import AIService
from app.models.database import init_db, Conversation, Metric

# Initialize FastAPI app
app = FastAPI()

# Initialize components
db = init_db()
analytics = AnalyticsEngine()
ai_service = None  # Will be initialized with API key

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    message: str
    api_key: str
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    processing_time: float
    success: bool

# Dependency to get AI service
async def get_ai_service(api_key: str):
    global ai_service
    if not ai_service or ai_service.llm.openai_api_key != api_key:
        ai_service = AIService(api_key)
    return ai_service

@app.get("/")
async def root():
    return {"message": "ANVE Customer Service AI API is running"}

@app.get("/health")
async def health_check():
    health_status = await analytics.get_system_health()
    return health_status

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start_time = time.time()
    
    try:
        # Get AI service instance
        service = await get_ai_service(request.api_key)
        
        # Process message
        result = await service.process_message(request.message, request.context)
        
        # Record metrics
        processing_time = time.time() - start_time
        await analytics.track_response_time("/chat", processing_time)
        await analytics.track_interaction(
            user_id="anonymous",  # You might want to add user authentication
            interaction_type="chat",
            details={
                "message_length": len(request.message),
                "response_length": len(result["response"]),
                "processing_time": processing_time
            }
        )
        
        if not result["success"]:
            await analytics.track_error("/chat", str(result["response"]))
            raise HTTPException(status_code=500, detail=result["response"])
        
        return ChatResponse(
            response=result["response"],
            processing_time=processing_time,
            success=True
        )
        
    except Exception as e:
        await analytics.track_error("/chat", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/metrics")
async def get_metrics(timeframe: str = "1h"):
    try:
        report = await analytics.generate_report(timeframe)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/health")
async def get_detailed_health():
    try:
        health = await analytics.get_system_health()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 