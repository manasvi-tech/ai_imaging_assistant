import pydicom
from PIL import Image
import numpy as np
import nibabel as nib
import os

def dicom_to_png(dicom_path: str, png_path: str):
    ds = pydicom.dcmread(dicom_path)
    pixel_array = ds.pixel_array

    # Remove all singleton dimensions
    pixel_array = np.squeeze(pixel_array)

    # If it's still 3D (volume), take the middle slice
    if pixel_array.ndim == 3:
        # (depth, height, width) or (height, width, depth)
        middle_index = pixel_array.shape[0] // 2
        pixel_array = pixel_array[middle_index]

    # Normalize to 0-255
    if pixel_array.max() > 0:
        pixel_array = (pixel_array / pixel_array.max()) * 255.0

    pixel_array = pixel_array.astype(np.uint8)

    # Convert to grayscale image
    image = Image.fromarray(pixel_array)
    image = image.convert("L")  # Ensure grayscale
    image.save(png_path)
    
def nifti_to_png(input_path, output_path):
    img = nib.load(input_path).get_fdata()
    img_slice = np.rot90(img[:, :, img.shape[2] // 2])
    img = Image.fromarray(img_slice).convert("L")
    img.save(output_path)
    return output_path
