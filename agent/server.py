from fastapi import FastAPI
from pydantic import BaseModel
from agent import (
    download_video,
    extract_frames,
    score_frames,
    generate_marketing_image,
    modify_image
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
    local_path = download_video(req.gcs_uri)
    frames = extract_frames(local_path)
    scored_frames = score_frames(frames)

    # Return top 4 frames
    top_frames = [{"score": s, "image_base64": img} for s, img in scored_frames[:4]]

    return {"frames": top_frames}


@app.post("/generate-image")
async def generate_image(req: GenerateReq):
    result = generate_marketing_image(req.frame_base64, req.platform)
    return result


@app.post("/modify-image")
async def modify_image_endpoint(req: ModifyReq):
    mod = modify_image(req.image_base64, req.prompt)
    return {"modified_image_base64": mod}
