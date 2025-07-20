import numpy as np
from monai.networks.nets import BasicUNet
from skimage.segmentation import watershed
from skimage.filters import sobel
from typing import Tuple

class CPUSegmentor:
    def __init__(self):
        self.model = self._init_monai_model()
        
    def _init_monai_model(self):
        """Lightweight UNet for CPU"""
        return BasicUNet(
            spatial_dims=2,
            in_channels=1,
            out_channels=1,
            features=(16, 16, 32),  # Reduced complexity
            dropout=0.1
        )
    
    def segment(self, pixel_array: np.ndarray) -> Tuple[np.ndarray, list]:
        """Run segmentation with fallback to watershed"""
        try:
            # MONAI inference
            with torch.no_grad():
                input_tensor = torch.from_numpy(pixel_array).unsqueeze(0).unsqueeze(0)
                output = self.model(input_tensor)
                mask = output.squeeze().numpy()
        except RuntimeError:
            # Fallback to traditional CV
            mask = self._watershed_segment(pixel_array)
            
        return mask, self._generate_annotations(mask)
    
    def _watershed_segment(self, image: np.ndarray) -> np.ndarray:
        """CPU-efficient alternative"""
        edges = sobel(image)
        markers = np.zeros_like(image)
        markers[image < np.percentile(image, 30)] = 1
        markers[image > np.percentile(image, 70)] = 2
        return watershed(edges, markers)
    
    def _generate_annotations(self, mask: np.ndarray) -> list:
        """Convert mask to text reports"""
        unique_regions = len(np.unique(mask)) - 1
        return [f"AI detected {unique_regions} anatomical regions"]