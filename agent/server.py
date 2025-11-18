from fastapi import FastAPI
from pydantic import BaseModel

from agent import (
    generate_marketing_image,
    modify_image,
    dummy_extract_frames,   # <-- using lightweight placeholder
)

app = FastAPI()

# ----------------------------
# Request Models
# ----------------------------

class ProcessVideoReq(BaseModel):
    gcs_uri: str
    platforms: list[str]


class GenerateReq(BaseModel):
    frame_base64: str
    platform: str


class ModifyReq(BaseModel):
    image_base64: str
    prompt: str


# ----------------------------
# Endpoints
# ----------------------------

@app.post("/process-video")
async def process_video(req: ProcessVideoReq):
    """
    Cloud Run cannot process real video (ffmpeg missing).
    So agent.py returns dummy frames using Gemini image generation.
    """
    frames = dummy_extract_frames()

    # Already returned as list of {"score": ..., "image_base64": ...}
    return {"frames": frames}


@app.post("/generate-image")
async def generate_image(req: GenerateReq):
    """
    Uses Gemini Flash 2.5 to generate a marketing image from a frame.
    """
    result = generate_marketing_image(req.frame_base64, req.platform)
    return result


@app.post("/modify-image")
async def modify_image_endpoint(req: ModifyReq):
    """
    Uses Gemini Flash 2.5 editing mode.
    """
    mod = modify_image(req.image_base64, req.prompt)
    return {"modified_image_base64": mod}
