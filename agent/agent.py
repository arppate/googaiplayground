import base64
import vertexai
from vertexai.generative_models import GenerativeModel

# -------------------------------------------------------------------
# INIT VERTEX
# -------------------------------------------------------------------
vertexai.init(project="neon-fiber-478418-e3", location="europe-west1")

# Load Gemini models
TEXT_MODEL = GenerativeModel("gemini-2.5-flash")
IMAGE_MODEL = GenerativeModel("gemini-2.5-flash-image")


# -------------------------------------------------------------------
# TEXT GENERATION
# -------------------------------------------------------------------
def generate_text(prompt: str) -> str:
    """Generate text using Gemini 2.5 Flash."""
    response = TEXT_MODEL.generate_content(prompt)
    return response.text


# -------------------------------------------------------------------
# IMAGE GENERATION
# -------------------------------------------------------------------
def generate_image(prompt: str, size: str = "1024x1024") -> bytes:
    """
    Generate an image using Gemini Flash 2.5 Image model.
    Returns raw image bytes.
    """
    response = IMAGE_MODEL.generate_image(
        prompt=prompt,
        size=size,
    )
    return response.images[0].bytes


# -------------------------------------------------------------------
# IMAGE EDITING
# -------------------------------------------------------------------
def edit_image(prompt: str, input_image_bytes: bytes, size: str = "1024x1024") -> bytes:
    """
    Edit an image using Gemini Flash 2.5 Image model.
    Returns edited image bytes.
    """
    response = IMAGE_MODEL.edit_image(
        prompt=prompt,
        image=input_image_bytes,
        size=size,
    )
    return response.images[0].bytes


# -------------------------------------------------------------------
# BASE64 HELPERS
# -------------------------------------------------------------------
def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def decode_base64_to_bytes(b64: str) -> bytes:
    return base64.b64decode(b64)
