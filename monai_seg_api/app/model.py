# app/model.py - CPU Optimized Version
import torch
import torch.nn as nn
from monai.networks.nets import UNet
from monai.transforms import Compose, Resize, ScaleIntensity, ToTensor
from monai.inferers import sliding_window_inference
import numpy as np
import os

class CPUOptimizedSegmentation:
    def __init__(self):
        # Force CPU usage
        self.device = torch.device("cpu")
        torch.set_num_threads(4)  # Use all 4 CPU cores
        
        # Use smaller, CPU-friendly model
        self.model = UNet(
            spatial_dims=2,  # Use 2D instead of 3D for speed
            in_channels=1,
            out_channels=2,
            channels=(16, 32, 64, 128),  # Smaller channels
            strides=(2, 2, 2),
            num_res_units=1,  # Reduced complexity
        ).to(self.device)
        
        # Set to evaluation mode
        self.model.eval()
        
        # CPU-optimized transforms
        self.transforms = Compose([
            Resize(spatial_size=(256, 256)),  # Smaller size for CPU
            ScaleIntensity(minv=0.0, maxv=1.0),
            ToTensor()
        ])
    
    def preprocess_image(self, image_array):
        """Optimize image for CPU processing"""
        # Convert to 2D slices if 3D
        if len(image_array.shape) == 3:
            # Take middle slice or process slice by slice
            middle_slice = image_array.shape[2] // 2
            image_array = image_array[:, :, middle_slice]
        
        # Add channel dimension
        if len(image_array.shape) == 2:
            image_array = image_array[np.newaxis, ...]
        
        return self.transforms(image_array)
    
    def segment(self, image_array):
        """CPU-optimized segmentation"""
        try:
            # Preprocess
            input_tensor = self.preprocess_image(image_array)
            input_tensor = input_tensor.unsqueeze(0).to(self.device)
            
            # Inference with CPU optimization
            with torch.no_grad():
                torch.set_num_threads(4)
                
                # Use smaller sliding window for CPU
                if input_tensor.shape[-1] > 256 or input_tensor.shape[-2] > 256:
                    output = sliding_window_inference(
                        input_tensor,
                        roi_size=(128, 128),  # Smaller ROI for CPU
                        sw_batch_size=1,
                        predictor=self.model,
                        overlap=0.25
                    )
                else:
                    output = self.model(input_tensor)
                
                # Get segmentation mask
                probabilities = torch.softmax(output, dim=1)
                segmentation = torch.argmax(probabilities, dim=1)
                
                return {
                    "segmentation": segmentation.cpu().numpy(),
                    "probabilities": probabilities.cpu().numpy(),
                    "success": True
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

# app/main.py - Updated FastAPI with longer timeouts
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import nibabel as nib
from io import BytesIO
import time

app = FastAPI(title="MONAI Segmentation API", version="1.0.0")

# Initialize model
segmentation_model = CPUOptimizedSegmentation()

@app.get("/health")
async def health_check():
    """Simple health check - no heavy computation"""
    return {"status": "healthy", "device": "cpu", "timestamp": time.time()}

@app.post("/segment")
async def segment_image(file: UploadFile = File(...)):
    """Segment uploaded medical image"""
    if not file.filename.endswith(('.nii', '.nii.gz')):
        raise HTTPException(status_code=400, detail="Only NIfTI files supported")
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Load NIfTI image
        nii_image = nib.load(BytesIO(contents))
        image_data = nii_image.get_fdata()
        
        # Perform segmentation
        start_time = time.time()
        result = segmentation_model.segment(image_data)
        processing_time = time.time() - start_time
        
        if result["success"]:
            return {
                "message": "Segmentation completed",
                "processing_time": processing_time,
                "input_shape": image_data.shape,
                "output_shape": result["segmentation"].shape,
                "unique_labels": np.unique(result["segmentation"]).tolist()
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "MONAI Segmentation API is running on CPU"}


