import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import cv2
import albumentations as A
from segmentation_models_pytorch import Unet
from planetarycomputer import api
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection

class SatelliteImageDataset(Dataset):
    """Dataset class for satellite imagery"""
    
    def __init__(self, image_paths: List[Path], transforms: Optional[A.Compose] = None):
        self.image_paths = image_paths
        self.transforms = transforms or self._get_default_transforms()
    
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        image_path = self.image_paths[idx]
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.transforms:
            transformed = self.transforms(image=image)
            image = transformed['image']
        
        return {'image': torch.from_numpy(image).permute(2, 0, 1)}
    
    @staticmethod
    def _get_default_transforms() -> A.Compose:
        """Default augmentation pipeline"""
        return A.Compose([
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            A.Resize(256, 256)
        ])

class SatelliteAnalyzer:
    """Analyzes satellite imagery for vegetation and burn detection"""
    
    def __init__(self, model_path: Optional[Path] = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._initialize_model()
        if model_path and model_path.exists():
            self.load_model(model_path)
        
        # Initialize Sentinel Hub configuration
        self.sh_config = SHConfig()
        if 'SENTINEL_HUB_API_KEY' in os.environ:
            self.sh_config.sh_client_id = os.environ['SENTINEL_HUB_API_KEY']
    
    def _initialize_model(self) -> nn.Module:
        """Initialize the U-Net model for segmentation"""
        model = Unet(
            encoder_name="resnet34",
            encoder_weights="imagenet",
            in_channels=3,
            classes=4  # [vegetation, burned, water, other]
        )
        return model.to(self.device)
    
    def fetch_satellite_data(self, bbox: List[float], date_range: Tuple[str, str]) -> np.ndarray:
        """Fetch Sentinel-2 satellite data for the given area and time range"""
        request = SentinelHubRequest(
            data_collection=DataCollection.SENTINEL2_L2A,
            bbox=bbox,
            time=(date_range[0], date_range[1]),
            config=self.sh_config
        )
        return request.get_data()
    
    def analyze_vegetation(self, image: np.ndarray) -> Dict[str, float]:
        """Calculate vegetation indices (NDVI, EVI) from satellite imagery"""
        nir_band = image[:, :, 3]  # Near-infrared band
        red_band = image[:, :, 2]  # Red band
        blue_band = image[:, :, 0]  # Blue band
        
        # Calculate NDVI (Normalized Difference Vegetation Index)
        ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
        
        # Calculate EVI (Enhanced Vegetation Index)
        evi = 2.5 * ((nir_band - red_band) / 
                     (nir_band + 6 * red_band - 7.5 * blue_band + 1))
        
        return {
            'ndvi_mean': float(np.mean(ndvi)),
            'ndvi_std': float(np.std(ndvi)),
            'evi_mean': float(np.mean(evi)),
            'evi_std': float(np.std(evi))
        }
    
    def detect_burn_scars(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect and analyze burn scars in the imagery"""
        dataset = SatelliteImageDataset([image])
        loader = DataLoader(dataset, batch_size=1, shuffle=False)
        
        self.model.eval()
        with torch.no_grad():
            for batch in loader:
                images = batch['image'].to(self.device)
                outputs = self.model(images)
                masks = torch.argmax(outputs, dim=1)
                
                # Calculate burn scar statistics
                burn_mask = (masks == 1).cpu().numpy()  # Class 1 is burn scars
                burn_area = np.sum(burn_mask)
                burn_perimeter = cv2.findContours(
                    burn_mask.astype(np.uint8), 
                    cv2.RETR_EXTERNAL, 
                    cv2.CHAIN_APPROX_SIMPLE
                )[0]
                
                return {
                    'burn_area_percentage': float(burn_area / burn_mask.size),
                    'burn_perimeter_length': float(sum(len(c) for c in burn_perimeter)),
                    'burn_mask': burn_mask
                }
    
    def save_model(self, path: Path) -> None:
        """Save model weights"""
        torch.save(self.model.state_dict(), path)
    
    def load_model(self, path: Path) -> None:
        """Load model weights"""
        self.model.load_state_dict(torch.load(path, map_location=self.device))
