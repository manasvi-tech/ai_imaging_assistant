import os
import google.generativeai as genai
import base64

from app.core.config import settings

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY)

def encode_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

import os
import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY)

def analyze_scan_with_gemini(image_path: str, age: int, scan_type: str):
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = (
        f"You are a radiology AI. The patient is {age} years old. "
        f"The scan type is {scan_type}. Analyze the scan image below and describe any findings, "
        f"possible abnormalities, and give a clinical impression."
    )

    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/png", "data": image_bytes}}
                ]
            }
        ]
    )

    return response.text

