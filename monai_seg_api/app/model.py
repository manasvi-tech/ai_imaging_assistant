import os
import torch
from monai.networks.nets import UNet
from monai.transforms import (
    Compose, LoadImage, EnsureChannelFirst, ScaleIntensity, Resize, ToTensor
)
import nibabel as nib
import numpy as np

# Inference function
def run_inference(image_path: str) -> str:
    model = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=2,
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
        num_res_units=2,
    )
    model.load_state_dict(torch.load("model/model.pth", map_location="cpu"))
    model.eval()

    transforms = Compose([
        LoadImage(image_only=True),
        EnsureChannelFirst(),
        ScaleIntensity(),
        Resize((128, 128, 128)),
        ToTensor()
    ])

    image = transforms(image_path).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(image)
        seg = torch.argmax(output, dim=1).squeeze().numpy()

    # Save segmentation mask as NIfTI
    output_path = image_path.replace(".nii.gz", "_seg.nii.gz")
    nib.save(nib.Nifti1Image(seg.astype(np.uint8), affine=np.eye(4)), output_path)

    return output_path

def run_inference(image_path: str) -> str:
    # Force CPU (even if CUDA is available)
    device = torch.device("cpu")
    
    model = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=2,
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
        num_res_units=2,
    ).to(device)  # <-- Explicitly move to CPU

    # Debug: Check if model.pth exists
    model_path = "/app/model/model.pth"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file missing at: {model_path}")
    
    model.load_state_dict(torch.load(model_path, map_location=device))  # <-- Load directly to CPU
    model.eval()

    # ... (rest of your code)
