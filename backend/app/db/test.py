import requests

API_URL = "https://api-inference.huggingface.co/models/MONAI/VISTA3D-HF"
headers = {
    "Authorization": f"Bearer YOUR_HF_API_KEY"
}

# You must upload a 3D image (e.g., .nii.gz or .dcm series converted to NIfTI)
with open("example_volume.nii.gz", "rb") as f:
    data = f.read()

response = requests.post(API_URL, headers=headers, data=data)

# Print the response (usually a link to download segmentation)
print(response.json())