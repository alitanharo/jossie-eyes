"""
Jossie Eyes - FastAPI Backend for Web UI
Provides REST API for image analysis, speech, and neural signal simulation
"""

import os
import sys
import base64
import json
import time
import random
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from brain_service import BrainService

# Initialize FastAPI app
app = FastAPI(
    title="Jossie Eyes API",
    description="API for Jossie Eyes - Neural Sensory Guide",
    version="2.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize brain service
brain_service = None

def get_brain_service():
    """Get or initialize brain service"""
    global brain_service
    if brain_service is None:
        brain_service = BrainService()
    return brain_service


# ==================== Models ====================

class AnalysisRequest(BaseModel):
    mode: str = "describe"
    question: Optional[str] = None

class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = ""

class SignalSimulation(BaseModel):
    description: str
    duration: float = 3.0


# ==================== Endpoints ====================

@app.get("/")
def root():
    """API health check"""
    return {"status": "ok", "message": "Jossie Eyes API is running"}

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "jossie-eyes-api"}

@app.post("/api/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    mode: str = Form(default="describe")
):
    """
    Analyze an uploaded image and return description
    
    Args:
        image: Image file (JPEG, PNG)
        mode: 'describe', 'ocr', or 'neural_simulation'
    
    Returns:
        Analysis result with description
    """
    try:
        # Read image data
        image_data = await image.read()
        
        # Get brain service and analyze
        brain = get_brain_service()
        result = brain.analyze_image(image_data, mode)
        
        if result['success']:
            # Generate simulated neural signals
            signals = generate_neural_signals(result['description'])
            result['signals'] = signals
            
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Analysis failed'))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question about a previously analyzed scene
    
    Args:
        question: User's question
        context: Optional context from previous analysis
    
    Returns:
        Answer from Jossie
    """
    try:
        brain = get_brain_service()
        result = brain.ask_question(request.question, request.context)
        
        if result['success']:
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Question failed'))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/speech")
async def text_to_speech(text: str = Form(...)):
    """
    Convert text to speech audio
    
    Args:
        text: Text to convert to speech
    
    Returns:
        Audio file (WAV format)
    """
    try:
        brain = get_brain_service()
        audio_data = brain.text_to_speech(text)
        
        if audio_data:
            # Save to temp file and return
            temp_path = f"/tmp/speech_{int(time.time())}.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_data)
            
            return FileResponse(
                temp_path,
                media_type="audio/wav",
                filename="speech.wav"
            )
        else:
            raise HTTPException(status_code=500, detail="Speech generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/signals/simulate")
def simulate_neural_signals(
    description: str,
    duration: float = 3.0
):
    """
    Generate simulated neural signals based on description
    
    This simulates what brain signals might look like when
    a visually impaired person receives visual information
    through the neural bridge.
    
    Returns:
        Simulated signal data for visualization
    """
    signals = generate_neural_signals(description, duration)
    return JSONResponse(content={
        "signals": signals,
        "duration": duration,
        "description": description
    })

@app.post("/api/reset")
def reset_conversation():
    """Reset conversation history"""
    try:
        brain = get_brain_service()
        brain.clear_conversation()
        return {"status": "ok", "message": "Conversation reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Helper Functions ====================

def generate_neural_signals(description: str, duration: float = 3.0) -> Dict[str, Any]:
    """
    Generate simulated neural signals based on description
    
    This creates realistic-looking brain signal patterns that would
    be sent to neural implants in a real implementation.
    """
    # Generate signal data points
    num_points = int(duration * 100)  # 100 points per second
    timestamps = [i / 100.0 for i in range(num_points)]
    
    # Simulate different brain wave patterns
    signals = {
        "alpha": [],  # Relaxed awareness (8-13 Hz)
        "beta": [],   # Active thinking (13-30 Hz)
        "gamma": [],  # Higher processing (30-100 Hz)
        "theta": []   # Deep relaxation (4-8 Hz)
    }
    
    # Base frequencies
    base_alpha = 10  # Hz
    base_beta = 20   # Hz
    base_gamma = 40  # Hz
    base_theta = 6   # Hz
    
    # Analyze description for signal intensity
    desc_lower = description.lower()
    intensity = 0.5
    
    # Increase intensity based on content
    if any(word in desc_lower for word in ["hazard", "danger", "obstacle", "warning", "careful"]):
        intensity = 0.8  # Higher alertness
    elif any(word in desc_lower for word in ["calm", "peaceful", "quiet", "relax"]):
        intensity = 0.3  # More relaxed
    
    for t in timestamps:
        # Generate wave patterns with noise
        alpha_val = (0.3 + 0.2 * intensity) * (
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * (t % 2)) +
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * ((t + 0.5) % 2))
        )
        
        beta_val = (0.2 + 0.3 * intensity) * (
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * (t % 1.5)) +
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * ((t + 0.3) % 1.5))
        )
        
        gamma_val = (0.1 + 0.15 * intensity) * (
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * (t % 0.8)) +
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * ((t + 0.2) % 0.8))
        )
        
        theta_val = (0.4 - 0.2 * intensity) * (
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * (t % 3)) +
            0.5 * (1 + 0.3 * random.gauss(0, 1)) * (1 + 0.5 * ((t + 1) % 3))
        )
        
        signals["alpha"].append(round(alpha_val, 4))
        signals["beta"].append(round(beta_val, 4))
        signals["gamma"].append(round(gamma_val, 4))
        signals["theta"].append(round(theta_val, 4))
    
    # Generate "brain image" - simulated visual cortex activation pattern
    brain_image = generate_brain_activation_pattern(description)
    
    return {
        "waveforms": signals,
        "brain_image": brain_image,
        "intensity": intensity,
        "duration": duration
    }

def generate_brain_activation_pattern(description: str) -> Dict[str, Any]:
    """
    Generate a simulated brain activation pattern
    This represents which areas of the visual cortex would be activated
    """
    # Create a grid representing brain activation
    grid_size = 20
    activation = []
    
    # Base activation pattern
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # Create a pattern based on position and description
            center_dist = ((i - 10)**2 + (j - 10)**2) ** 0.5
            base_activation = max(0, 1 - center_dist / 10)
            
            # Add some variation based on description
            desc_hash = hash(description + str(i) + str(j))
            variation = (desc_hash % 100) / 100 * 0.3
            
            row.append(round(base_activation + variation, 4))
        activation.append(row)
    
    return {
        "grid": activation,
        "size": grid_size,
        "max_activation": max(max(row) for row in activation),
        "focal_point": [10, 10]  # Center of activation
    }


# ==================== Main Entry Point ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)