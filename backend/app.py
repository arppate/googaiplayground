import cv2
import base64
import tempfile
import numpy as np
from vertexai import init as vertex_init
from vertexai.generative_models import GenerativeModel

vertex_init()

MODEL = GenerativeModel("gemini-2.0-flash")


# ----------------------------------------------------
# Download GCS video
# ----------------------------------------------------
from google.cloud import storage

storage_client = storage.Client()

def download_video(gcs_uri):
    bucket_name = gcs_uri.split("/")[2]
    path = "/".join(gcs_uri.split("/")[3:])
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    blob.download_to_filename(tmp.name)
    return tmp.name


# ----------------------------------------------------
# Extract frames with OpenCV
# ----------------------------------------------------
def extract_frames(video_path, num_frames=8):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total == 0:
        return []

    frames = []
    interval = max(total // num_frames, 1)

    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if not ret:
            continue

        # resize for speed
        frame = cv2.resize(frame, (512, 512))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buf = cv2.imencode(".jpg", frame_rgb)
        b64 = base64.b64encode(buf).decode("utf-8")

        frames.append(b64)

    cap.release()
    return frames


# ----------------------------------------------------
# Score frames (simple)
# ----------------------------------------------------
def score_frames(frames):
    return [{"score": round(np.random.uniform(0.8, 1.0), 2), "image_base64": f} for f in frames]


# ----------------------------------------------------
# Generate image with Gemini
# ----------------------------------------------------
def generate_marketing_image(frame_base64, platform):
    img_bytes = base64.b64decode(frame_base64)

    response = MODEL.generate_content(
        [
            {"mime_type": "image/jpeg", "data": img_bytes},
            f"Generate a marketing-style product ad optimized for {platform}."
        ]
    )

    out_bytes = response.candidates[0].content.parts[0].data
    out_b64 = base64.b64encode(out_bytes).decode("utf-8")
    return {"image_base64": out_b64}


# ----------------------------------------------------
# Modify image
# ----------------------------------------------------
def modify_image(image_base64, prompt):
    img = base64.b64decode(image_base64)

    response = MODEL.generate_content(
        [
            {"mime_type": "image/jpeg", "data": img},
            f"Modify the image with this instruction: {prompt}"
        ]
    )

    out_bytes = response.candidates[0].content.parts[0].data
    return base64.b64encode(out_bytes).decode("utf-8")
