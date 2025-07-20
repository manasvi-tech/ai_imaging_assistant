from .models.segmentation import CPUSegmentor
from ..storage import get_dicom_pixels  # Your existing service

from ..schemas.scan import ScanCreate
from ..db import get_db

class AIService:
    def __init__(self):
        self.segmentor = CPUSegmentor()
    
    async def segment_scan(self, scan_id: UUID) -> dict:
        """Orchestrates the full segmentation flow"""
        db = next(get_db())
        
        # 1. Get DICOM from your storage service
        dicom_path = await get_dicom_path(scan_id)  
        pixel_array = get_dicom_pixels(dicom_path)
        
        # 2. Run inference
        mask, annotations = self.segmentor.segment(pixel_array)
        
        # 3. Save to database (extend your Scan model)
        scan_update = ScanCreate(
            segmentation_mask=mask.tolist(),
            ai_annotations=annotations
        )
        db.scans.update(scan_id, scan_update)
        
        return {
            "scan_id": scan_id,
            "mask_shape": mask.shape,
            "annotations": annotations
        }