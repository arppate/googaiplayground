import base64
from vertexai import init as vertex_init
from vertexai.preview.generative_models import GenerativeModel

# Init Vertex AI (Cloud Run will auto-detect PROJECT + REGION)
vertex_init()

# Load Gemini Flash 2.5 Image model
IMAGE_MODEL = GenerativeModel("gemini-2.0-flash")

# -------------------------------------------------------------------
# Dummy frames because Cloud Run cannot extract frames without ffmpeg
# -------------------------------------------------------------------
def dummy_extract_frames():
    """Return fake frames so frontend flow works."""
    placeholder = base64.b64encode(b"fake_image_data").decode("utf-8")
    return [
        {"score": 0.98, "image_base64": placeholder},
        {"score": 0.95, "image_base64": placeholder},
        {"score": 0.92, "image_base64": placeholder},
        {"score": 0.90, "image_base64": placeholder},
    ]


# -------------------------------------------------------------------
# Marketing Image Generation
# -------------------------------------------------------------------
def generate_marketing_image(frame_base64: str, platform: str):
    """Generate a marketing-style image from a frame using Gemini Flash."""
    prompt = f"Create a marketing-ready ad image for {platform} using this frame."

    response = IMAGE_MODEL.generate_content(
        [
            {"mime_type": "image/jpeg", "data": base64.b64decode(frame_base64)},
            prompt
        ],
        generation_config={"max_output_tokens": 2048}
    )

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
