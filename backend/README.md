
---

# **📁 backend/README.md**

```markdown
# Backend – Smart Video Repurposer

This backend is responsible for:
- Generating **presigned URLs** for video upload to GCS
- Extracting frames using Gemini Video APIs
- Connecting to NanoBanana for image editing
- Serving APIs for the frontend & agent

---

## ⚙️ Tech Stack
- **FastAPI** (Python) or Node.js (your actual choice)
- **Google Cloud Storage**
- **Google AI Gemini APIs**
- **NanoBanana (Gemini 2.5 Flash Image)**

---

## 🚀 Endpoints Overview

### `POST /upload-url`
Returns a presigned URL for uploading a video.

### `POST /extract-frames`
Extracts key frames using Gemini Video and returns them.

### `POST /edit-image`
Sends image + prompt → modifies using NanoBanana.

### `POST /generate-content`
Platform-specific content generation (via agent or directly).

---

## 📂 Folder Structure
backend/
├── main.py
├── services/
│ ├── gcs.py
│ ├── gemini.py
│ └── nanobanana.py
└── utils/


---

## 🧪 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt

###2: Create .env:

GCP_BUCKET_NAME=your-bucket
GCP_PROJECT_ID=your-project
GOOGLE_API_KEY=your-key

###3: uvicorn main:app --reload
