from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from .model import load_model, predict
from .schemas import PredictionInput
import logging

app = FastAPI(title="MONAI Assignment API")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model at startup
@app.on_event("startup")
async def startup_event():
    try:
        load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}")
        raise

@app.post("/predict", response_model=dict)
async def predict_endpoint(input_data: PredictionInput):
    try:
        logger.info(f"Received prediction request")
        result = predict(input_data)
        return {"prediction": result, "status": "success"}
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

@app.get("/health")
async def health_check():
    import torch
    return {
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    }