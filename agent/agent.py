import base64
import cv2
import tempfile
from google.cloud import storage
from vertexai import init as vertex_init
from vertexai.preview.generative_models import GenerativeModel

# Init Vertex AI (Cloud Run will auto-detect PROJECT + REGION)
vertex_init()

# Load Gemini Flash 2.5 Image model
IMAGE_MODEL = GenerativeModel("gemini-2.0-flash")


# -------------------------------------------------------------------
# Download Video from GCS
# -------------------------------------------------------------------
def download_video(gcs_uri: str) -> str:
    """
    gcs_uri format: gs://bucket/path/video.mp4
    Downloads to a temp local file.
    """
    assert gcs_uri.startswith("gs://")
    _, bucket_name, *blob_parts = gcs_uri.split("/")
    blob_name = "/".join(blob_parts)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    blob.download_to_filename(tmp.name)
    return tmp.name


# -------------------------------------------------------------------
# Extract Frames (REAL extraction)
# -------------------------------------------------------------------
def extract_frames(video_path: str, frame_interval=30):
    """
    Extract frames every N frames (default = every 30 frames ~ 1 second).
    Returns list of base64-encoded JPEG frames.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0
    success, frame = cap.read()

    while success:
        if idx % frame_interval == 0:
            ret, buffer = cv2.imencode(".jpg", frame)
            if ret:
                encoded = base64.b64encode(buffer).decode("utf-8")
                frames.append(encoded)

        success, frame = cap.read()
        idx += 1

    cap.release()
    return frames


# -------------------------------------------------------------------
# Score Frames (simple heuristic)
# -------------------------------------------------------------------
def score_frames(frames):
    """
    Give simple default score.
    You can improve scoring later.
    """
    scored = []
    for f in frames:
        scored.append((0.5, f))
    return scored


# -------------------------------------------------------------------
# Marketing Image Generation
# -------------------------------------------------------------------
def generate_marketing_image(frame_base64: str, platform: str):
    """Generate a marketing-style image from a frame using Gemini Flash."""
    prompt = f"Create a marketing-ready ad image for {platform} using this video frame."

    response = IMAGE_MODEL.generate_content(
        [
            {"mime_type": "image/jpeg", "data": base64.b64decode(frame_base64)},
            prompt
        ],
        generation_config={"max_output_tokens": 2048}
    )

    # Extract first image output
    image_bytes = response.candidates[0].content.parts[0].data
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    return {"image_base64": img_b64}


# -------------------------------------------------------------------
# Image Modification
# -------------------------------------------------------------------
def modify_image(image_base64: str, prompt: str):
    """Modify an existing image using Gemini Flash 2.5."""
    response = IMAGE_MODEL.generate_content(
        [
            {"mime_type": "image/jpeg", "data": base64.b64decode(image_base64)},
            prompt
        ],
        generation_config={"max_output_tokens": 2048}
    )

    modified_bytes = response.candidates[0].content.parts[0].data
    mod_b64 = base64.b64encode(modified_bytes).decode("utf-8")

    return mod_b64


# -------------------------------------------------------------------
# Pipeline Entry: Process Video
# -------------------------------------------------------------------
def process_video_pipeline(gcs_uri: str):
    """
    Download video → extract frames → score frames → return top 4.
    """
    local_path = download_video(gcs_uri)
    frames = extract_frames(local_path)
    scored = score_frames(frames)

    # Get top 4 frames
    top = sorted(scored, key=lambda x: x[0], reverse=True)[:4]

    return [
        {"score": s, "image_base64": img}
        for s, img in top
    ]
