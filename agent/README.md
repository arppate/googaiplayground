# Clip2Campaign – Agent Microservice

This Cloud Run service powers the ADK conversational agent that:
- Accepts a video URI (GCS)
- Extracts frames using OpenCV
- Scores frames using Gemini 2.0 Flash
- Lets the user select the best frame in ADK chat UI
- Generates platform-specific marketing images using Gemini 2.5 Flash Image
- Allows post-editing via user prompt (Gemini 2.5 Flash Image)

Endpoints:
POST /process-video
POST /generate-image
POST /modify-image

Deploy:
gcloud builds submit --tag gcr.io/<PROJECT_ID>/clip2campaign-agent
gcloud run deploy clip2campaign-agent --image gcr.io/<PROJECT_ID>/clip2campaign-agent --region us-central1 --platform managed
