from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from google.cloud import storage
import uuid
import os

app = FastAPI()

BUCKET_NAME = os.getenv("VIDEO_BUCKET", "clip2campaign-videos")

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    # Validate
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file")

    # Generate unique ID
    video_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    blob_name = f"videos/{video_id}.{file_extension}"

    try:
        # Upload to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)

        blob.upload_from_file(file.file, content_type=file.content_type)

        gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"

        return JSONResponse(content={
            "video_id": video_id,
            "gcs_uri": gcs_uri
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from google.cloud import storage
import uuid
import os

app = FastAPI()

BUCKET_NAME = os.getenv("VIDEO_BUCKET", "clip2campaign-videos")

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    # Validate
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file")

    # Generate unique ID
    video_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    blob_name = f"videos/{video_id}.{file_extension}"

    try:
        # Upload to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)

        blob.upload_from_file(file.file, content_type=file.content_type)

        gcs_uri = f"gs://{BUCKET_NAME}/{blob_name}"

        return JSONResponse(content={
            "video_id": video_id,
            "gcs_uri": gcs_uri
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
