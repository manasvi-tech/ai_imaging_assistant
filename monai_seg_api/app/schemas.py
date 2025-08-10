from pydantic import BaseModel, conlist
from typing import List, Optional

class PredictionInput(BaseModel):
    array: List[List[List[float]]]  # 3D array for medical images
    metadata: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "array": [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]],
                "metadata": {"patient_id": "123"}
            }
        }