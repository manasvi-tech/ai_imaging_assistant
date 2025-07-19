import pydicom
import nibabel as nib
import numpy as np
from PIL import Image
import os

def dicom_to_png(dicom_path, output_path):
    """Convert DICOM file to PNG"""
    try:
        ds = pydicom.dcmread(dicom_path)
        img_array = ds.pixel_array
        
        # Normalize and convert to 8-bit
        img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype(np.uint8)
        
        # Handle different color channels
        if len(img_array.shape) == 2:  # Grayscale
            img = Image.fromarray(img_array)
        elif len(img_array.shape) == 3:  # RGB
            img = Image.fromarray(img_array, 'RGB')
        
        img.save(output_path)
        return True
    except Exception as e:
        raise Exception(f"DICOM conversion failed: {str(e)}")

def nifti_to_png(nifti_path, output_path, slice_index=None):
    """Convert NIfTI file to PNG (middle slice by default)"""
    try:
        img = nib.load(nifti_path)
        data = img.get_fdata()
        
        # If no slice specified, use middle slice
        if slice_index is None:
            slice_index = data.shape[-1] // 2
        
        # Get 2D slice
        if len(data.shape) == 3:
            slice_data = data[:, :, slice_index]
        elif len(data.shape) == 4:
            slice_data = data[:, :, slice_index, 0]  # First volume for 4D data
        else:
            slice_data = data  # Assume already 2D
        
        # Normalize and convert to 8-bit
        slice_data = ((slice_data - slice_data.min()) / (slice_data.max() - slice_data.min()) * 255).astype(np.uint8)
        
        Image.fromarray(slice_data).save(output_path)
        return True
    except Exception as e:
        raise Exception(f"NIfTI conversion failed: {str(e)}")