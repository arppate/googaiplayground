from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import storage
import uuid
import os

app = FastAPI()
BUCKET_NAME = os.getenv("VIDEO_BUCKET", "clip2campaign-videos")

# 1) GENERATE SIGNED URL
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
            expiration=900,
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


# 2) REGISTER VIDEO AFTER UPLOAD
class VideoMetadata(BaseModel):
    gcs_path: str
    video_id: str

@app.post("/upload-video")
def register_video(meta: VideoMetadata):
    return {
        "video_id": meta.video_id,
        "gcs_uri": f"gs://{BUCKET_NAME}/{meta.gcs_path}"
    }
