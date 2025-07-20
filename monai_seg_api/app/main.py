from fastapi import FastAPI, UploadFile, File
from app.model import run_inference
import shutil, os

app = FastAPI()

@app.post("/segment")
async def segment_image(file: UploadFile = File(...)):
    input_path = f"/tmp/{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = run_inference(input_path)
    return {"segmentation_mask": output_path}
