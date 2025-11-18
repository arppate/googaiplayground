from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import storage
import uuid
import os
import requests

app = FastAPI()

# ----------------------------
# Configuration
# ----------------------------

BUCKET_NAME = os.getenv("VIDEO_BUCKET", "clip2campaign-videos")
AGENT_URL = os.getenv(
    "AGENT_URL", 
    "https://clip2campaign-agent-770831665204.europe-west1.run.app"
)

# ----------------------------
# 1) Generate Signed Upload URL
# ----------------------------

@app.get("/generate-upload-url")
def generate_upload_url():
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        video_id = str(uuid.uuid4())
        blob_name = f"videos/{video_id}.mp4"
        blob = bucket.blob(blob_name)

        upload_url = blob.generate_signed_url(
            version="v4",
            expiration=900,  # 15 min
            method="PUT",
            content_type="video/mp4",
        )

        return {
            "upload_url": upload_url,
            "gcs_path": blob_name,
            "video_id": video_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# 2) Register uploaded video
# ----------------------------

class VideoMetadata(BaseModel):
    gcs_path: str
    video_id: str

@app.post("/upload-video")
def register_video(meta: VideoMetadata):

    # return info to frontend
    return {
        "video_id": meta.video_id,
        "gcs_uri": f"gs://{BUCKET_NAME}/{meta.gcs_path}"
    }


# ----------------------------
# 3) Forwarding: Process Video (calls Agent)
# ----------------------------

class ProcessReq(BaseModel):
    gcs_uri: str
    platforms: list[str]

@app.post("/process-video")
def process_video(req: ProcessReq):
    try:
        agent_resp = requests.post(
            f"{AGENT_URL}/process-video",
            json=req.dict(),
            timeout=300,
        )
        return agent_resp.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# 4) Forwarding: Generate Image (calls Agent)
# ----------------------------

class GenerateReq(BaseModel):
    frame_base64: str
    platform: str

@app.post("/generate-image")
def generate_image(req: GenerateReq):
    try:
        agent_resp = requests.post(
            f"{AGENT_URL}/generate-image",
            json=req.dict(),
            timeout=300,
        )
        return agent_resp.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# 5) Forwarding: Modify Image (calls Agent)
# ----------------------------

class ModifyReq(BaseModel):
    image_base64: str
    prompt: str

@app.post("/modify-image")
def modify_image(req: ModifyReq):
    try:
        agent_resp = requests.post(
            f"{AGENT_URL}/modify-image",
            json=req.dict(),
            timeout=300,
        )
        return agent_resp.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
