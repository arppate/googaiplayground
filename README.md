# Backend Upload Service

A minimal API that accepts a video upload and stores it in Google Cloud Storage.
Returns a GCS URI used by the AI Agent (ADK).

## Endpoints

POST /upload-video
- Accepts multipart/form-data
- Returns:
  {
    "video_id": "uuid",
    "gcs_uri": "gs://bucket/videos/<id>.mp4"
  }

## Deploy to Cloud Run

gcloud builds submit --tag gcr.io/<PROJECT_ID>/backend-upload

gcloud run deploy backend-upload \
  --image gcr.io/<PROJECT_ID>/backend-upload \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars VIDEO_BUCKET=clip2campaign-videos
