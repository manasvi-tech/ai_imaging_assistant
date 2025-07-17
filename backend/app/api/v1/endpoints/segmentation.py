from fastapi import APIRouter, UploadFile, File, Depends
from app.api.utils.image_converter import dicom_to_png, nifti_to_png
from app.services.ai.segmentation import run_segmentation_on_image
import os
import uuid

router = APIRouter()

@router.post("/segment/")
async def segment_image(scan_file: UploadFile = File(...)):
    # Save temp upload
    ext = scan_file.filename.split(".")[-1]
    temp_input_path = f"temp_upload_{uuid.uuid4()}.{ext}"
    temp_output_path = f"temp_converted_{uuid.uuid4()}.png"

    with open(temp_input_path, "wb") as f:
        f.write(await scan_file.read())

    # Convert
    if ext.lower() == "dcm":
        png_path = dicom_to_png(temp_input_path, temp_output_path)
    elif ext.lower() in ["nii", "gz", "nii.gz"]:
        png_path = nifti_to_png(temp_input_path, temp_output_path)
    else:
        raise ValueError("Unsupported file type")

    # Segment
    result = run_segmentation_on_image(png_path)

    # Clean up
    os.remove(temp_input_path)
    os.remove(temp_output_path)

    return {"segmentation_result": result}
