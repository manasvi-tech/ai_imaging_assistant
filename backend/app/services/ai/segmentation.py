from dotenv import load_dotenv
load_dotenv()

import os
import base64
import requests
from PIL import Image
from app.core.config import settings  # assumes settings.HF_TOKEN is defined

HF_API_URL = "https://api-inference.huggingface.co/models/flaviagiammarino/medsam-vit-base"
HF_TOKEN = os.getenv("HF_TOKEN") or settings.HF_TOKEN

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def get_image_base64(image_path: str):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_image_dimensions(image_path: str):
    with Image.open(image_path) as img:
        return img.size  # returns (width, height)


def call_medsam_segmentation(image_path: str):
    width, height = get_image_dimensions(image_path)
    image_base64 = get_image_base64(image_path)

    payload = {
        "inputs": {
            "image": image_base64,
            "boxes": [[0, 0, width, height]],
            "original_size": [height, width]
        },
        # optionally add parameters the Pipeline supports:
        "options": {
        "use_gpu": True
        }
    }

    response = requests.post(
        HF_API_URL,
        json=payload,
        headers=headers,
        timeout=60
    )

    if response.status_code != 200:
        raise ValueError(f"Segmentation API failed: {response.text}")

    return response.json()
