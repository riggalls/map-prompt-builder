from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Map Prompt Builder", 
    version="1.0.0",
    servers=[
        {"url": "https://map-prompt-builder-production.up.railway.app", "description": "Production server"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

class MapPromptIn(BaseModel):
    terrain: str
    encounter: str
    feature: Optional[str] = None
    grid_size: Optional[int] = 30
    style: Optional[str] = "OSR"
    color_tone: Optional[str] = "muted"
    vtt_ready: Optional[bool] = True
    extra_tags: Optional[str] = None

@app.post("/map-prompt")
def map_prompt(req: MapPromptIn):
    parts = [
        "Top-down TTRPG battle map",
        f"of {req.terrain}" + (f" with {req.feature}" if req.feature else ""),
        f"{req.style} style" if req.style else "",
        f"{req.color_tone} colors" if req.color_tone else "",
        f"{req.encounter} present",
        f"grid-aligned, {req.grid_size}x{req.grid_size} squares" if req.grid_size else "gridless",
        "playable for VTT" if req.vtt_ready else "",
        (req.extra_tags or "")
    ]
    prompt = ", ".join([p for p in parts if p]).replace(" ,", ",")
    return {"prompt": prompt}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Map Prompt Builder API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/privacy")
async def privacy_policy():
    """Privacy policy for Custom GPT Actions"""
    return {
        "privacy_policy": {
            "data_collection": {
                "what_we_collect": [
                    "Map generation parameters (terrain, encounter, features, etc.)",
                    "Style preferences (art style, color tone, grid size)",
                    "Optional descriptive tags and customizations"
                ],
                "what_we_dont_collect": [
                    "Personal identification information",
                    "User account data",
                    "Location information",
                    "Browsing history or cookies"
                ]
            },
            "data_usage": {
                "primary_purpose": "Generate TTRPG battle map prompts based on user specifications",
                "processing": "Input parameters are processed to create optimized prompts for AI image generation",
                "no_ai_training": "Data is not used to train or improve AI models",
                "no_profiling": "No user profiling or behavioral analysis is performed"
            },
            "data_retention": {
                "storage": "No data is permanently stored",
                "processing": "Data exists only during the API request/response cycle",
                "logs": "No persistent logs of user requests are maintained",
                "duration": "Data is discarded immediately after prompt generation"
            },
            "data_sharing": {
                "third_parties": "No data is shared with any third parties",
                "openai": "Data is only transmitted to OpenAI's Custom GPT system as part of the API response",
                "external_services": "No external services or APIs receive user data",
                "commercial_use": "No data is sold or used for commercial purposes"
            },
            "security": {
                "encryption": "All API communications use HTTPS encryption",
                "access": "No user data is accessible to external parties",
                "compliance": "This service is designed for personal TTRPG use only"
            },
            "contact": {
                "questions": "For privacy questions, contact the API provider",
                "updates": "This policy may be updated - check this endpoint for changes"
            }
        }
    }
