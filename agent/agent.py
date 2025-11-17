import base64
import cv2
import os
import tempfile
from vertexai.preview import generative_models, images
from vertexai.preview.generative_models import GenerativeModel
from google.cloud import storage

# Initialize Gemini models
gemini_text = GenerativeModel("gemini-2.0-flash")
# For image modification / generation
IMAGE_MODEL = "gemini-2.5-flash-image"

storage_client = storage.Client()


# -------------------------------
# 1. Download Video From GCS
# -------------------------------
def download_video(gcs_uri: str) -> str:
    assert gcs_uri.startswith("gs://")

    bucket_name = gcs_uri.split("/")[2]
    blob_path = "/".join(gcs_uri.split("/")[3:])

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    blob.download_to_filename(tmp.name)

    return tmp.name


# -------------------------------
# 2. Extract Frames
# -------------------------------
def extract_frames(video_path: str, max_frames: int = 6):
    vidcap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // max_frames)

    for i in range(0, total_frames, interval):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, image = vidcap.read()
        if not success:
            break
        frames.append(image)

    vidcap.release()
    return frames


# -------------------------------
# 3. Score Frames With Gemini Vision
# -------------------------------
def score_frames(frames):
    results = []
    for i, frame in enumerate(frames):
        # Convert OpenCV frame to base64
        _, buf = cv2.imencode(".jpg", frame)
        img_b64 = base64.b64encode(buf).decode()

        # Ask Gemini for "marketing suitability"
        prompt = """
        Rate this frame for its suitability as a marketing hero image.
        Give a score from 1 to 10.
        """

        response = gemini_text.generate_content(
            [
                prompt,
                generative_models.Part.from_data(
                    base64.b64decode(img_b64), mime_type="image/jpeg"
                ),
            ]
        )

        score = extract_score(response.text)
        results.append((score, img_b64))

    # Descending score
    results.sort(key=lambda x: x[0], reverse=True)
    return results


def extract_score(text):
    try:
        for tok in text.split():
            if tok.isdigit():
                return int(tok)
    except:
        pass
    return 5  # fallback default


# -------------------------------
# 4. Generate a Marketing Image
# -------------------------------
def generate_marketing_image(frame_base64: str, platform: str):
    img_bytes = base64.b64decode(frame_base64)

    prompt = f"""
    Create a polished, platform-specific marketing asset for {platform}.
    Keep the main subject intact but enhance color, lighting and add subtle branded style.
    """

    result = images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        image=img_bytes,
    )

    out_b64 = base64.b64encode(result.image_bytes).decode()

    return {
        "generated_image_base64": out_b64,
        "caption": f"Optimized caption for {platform}",
        "tagline": f"Engaging {platform} ready tagline",
        "prompt_used": prompt
    }


# -------------------------------
# 5. Modify Image (Gemini Flash Image)
# -------------------------------
def modify_image(image_base64: str, user_prompt: str):
    img_bytes = base64.b64decode(image_base64)

    result = images.edit(
        model=IMAGE_MODEL,
        image=img_bytes,
        prompt=user_prompt,
    )

    modified_b64 = base64.b64encode(result.image_bytes).decode()
    return modified_b64
