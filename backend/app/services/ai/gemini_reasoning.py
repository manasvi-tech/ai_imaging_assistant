import os
import io
import base64
import logging
from PIL import Image
import google.generativeai as genai

from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY)

def compress_image_to_bytes(image_path, target_size=(512, 512)) -> bytes:
    """Resize image to reduce payload and return as PNG bytes."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def analyze_scan_with_gemini(image_path: str, age: int, scan_type: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        f"Give report for {scan_type}. Analyze the scan image below and describe any findings, "
        f"possible abnormalities, and give a clinical impression."
    )

    compressed_image_bytes = compress_image_to_bytes(image_path)

    try:
        response = model.generate_content(
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64.b64encode(compressed_image_bytes).decode("utf-8")
                            }
                        }
                    ]
                }
            ],
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 512
            }
        )

        # Check if Gemini gave any text back
        if not hasattr(response, "text") or not response.text.strip():
            raise ValueError("Empty or invalid response from Gemini.")

        return response.text.strip()

    except Exception as e:
        logger.exception("Gemini reasoning failed.")
        raise RuntimeError(f"Gemini API error: {str(e)}")
