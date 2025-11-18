import base64
import cv2
import os
import tempfile
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel, ImageEditingModel
from google.cloud import storage

# Initialize Gemini models
gemini_text = GenerativeModel("gemini-2.0-flash")

# New image models
gen_model = ImageGenerationModel.from_pretrained("gemini-2.5-flash-image")
edit_model = ImageEditingModel.from_pretrained("gemini-2.5-flash-image")

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
# 3. Score Frames
# -------------------------------
def score_frames(frames):
    results = []
    for i, frame in enumerate(frames):
        _, buf = cv2.imencode(".jpg", frame)
        img_b64 = base64.b64encode(buf).decode()

        prompt = """
        Rate this frame for its suitability as a marketing hero image.
        Give a score from 1 to 10.
        """

        response = gemini_text.generate_content(
            [
                prompt,
                # Image part stays same
                generative_models.Part.from_data(
                    base64.b64decode(img_b64),
                    mime_type="image/jpeg"
                ),
            ]
        )

        score = extract_score(response.text)
        results.append((score, img_b64))

    results.sort(key=lambda x: x[0], reverse=True)
    return results


def extract_score(text):
    for tok in text.split():
        if tok.isdigit():
            return int(tok)
    return 5


# -------------------------------
# 4. Generate Marketing Image
# -------------------------------
def generate_marketing_image(frame_base64: str, platform: str):
    img_bytes = base64.b64decode(frame_base64)

    prompt = f"""
    Create a polished, platform-specific marketing asset for {platform}.
    Enhance lighting and color. Preserve main subject.
    """

    result = gen_model.generate_image(
        prompt=prompt,
        image=img_bytes,
    )

    out_b64 = base64.b64encode(result.image_bytes).decode()

    return {
        "generated_image_base64": out_b64,
        "caption": f"Optimized caption for {platform}",
        "tagline": f"Engaging {platform} ready tagline",
        "prompt_used": prompt,
    }


# -------------------------------
# 5. Modify Image
# -------------------------------
def modify_image(image_base64: str, user_prompt: str):
    img_bytes = base64.b64decode(image_base64)

    result = edit_model.edit_image(
        prompt=user_prompt,
        image=img_bytes,
    )

    modified_b64 = base64.b64encode(result.image_bytes).decode()
    return modified_b64
