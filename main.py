from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Map Prompt Builder", version="1.0.0")

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
