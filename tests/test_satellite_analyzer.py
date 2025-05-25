import numpy as np
import torch
import pytest
import cv2
import albumentations as A
from pathlib import Path
from app.cv.satellite_analyzer import SatelliteImageDataset, SatelliteAnalyzer


def test_get_default_transforms():
    transforms = SatelliteImageDataset._get_default_transforms()
    assert isinstance(transforms, A.Compose)
    types = [type(t) for t in transforms.transforms]
    assert A.Normalize in types
    assert A.Resize in types


def test_dataset_len_and_getitem(tmp_path):
    # create a dummy color image
    img = np.ones((10, 10, 3), dtype=np.uint8) * 127
    file = tmp_path / 'test.jpg'
    cv2.imwrite(str(file), img)
    ds = SatelliteImageDataset([file])
    assert len(ds) == 1
    sample = ds[0]
    assert 'image' in sample
    tensor = sample['image']
    assert isinstance(tensor, torch.Tensor)
    # default transforms include Resize to 256x256 and Normalize
    assert tensor.shape == (3, 256, 256)
    # values should be floats
    assert tensor.dtype.is_floating_point


def test_analyze_vegetation():
    # build a 2x2 image with 4 channels
    image = np.zeros((2, 2, 4), dtype=float)
    image[:, :, 3] = 4.0  # NIR
    image[:, :, 2] = 2.0  # Red
    image[:, :, 0] = 1.0  # Blue
    analyzer = SatelliteAnalyzer(model_path=None)
    veg = analyzer.analyze_vegetation(image)
    expected_ndvi = (4.0 - 2.0) / (4.0 + 2.0 + 1e-8)
    assert veg['ndvi_mean'] == pytest.approx(expected_ndvi)
    assert veg['ndvi_std'] == pytest.approx(0.0)
    expected_evi = 2.5 * ((4.0 - 2.0) / (4.0 + 6 * 2.0 - 7.5 * 1.0 + 1.0))
    assert veg['evi_mean'] == pytest.approx(expected_evi)
    assert veg['evi_std'] == pytest.approx(0.0)


def test_detect_burn_scars(monkeypatch):
    import app.cv.satellite_analyzer as sa
    # prepare a dummy image (2x2 RGB)
    dummy_img = np.zeros((2, 2, 3), dtype=np.uint8)
    # override dataset to return the image tensor directly
    class DummyDataset:
        def __init__(self, images):
            self.images = images
        def __len__(self):
            return 1
        def __getitem__(self, idx):
            img_tensor = torch.from_numpy(self.images).permute(2, 0, 1).float()
            return {'image': img_tensor}
    monkeypatch.setattr(sa, 'SatelliteImageDataset', DummyDataset)
    # override DataLoader to yield the one sample
    class DummyLoader:
        def __init__(self, dataset, batch_size, shuffle):
            self.dataset = dataset
        def __iter__(self):
            # batch must have 'image' key with shape [1,C,H,W]
            sample = self.dataset[0]
            batch = {'image': sample['image'].unsqueeze(0)}
            return iter([batch])
    monkeypatch.setattr(sa, 'DataLoader', DummyLoader)
    # stub model to output two classes, with class 1 at (0,0)
    class DummyModel:
        def eval(self):
            pass
        def __call__(self, x):
            b, c, h, w = x.shape
            out = torch.zeros(b, 2, h, w)
            out[:, 1, 0, 0] = 1.0
            return out
    analyzer = SatelliteAnalyzer(model_path=None)
    analyzer.model = DummyModel()
    # stub cv2.findContours
    monkeypatch.setattr(cv2, 'findContours', lambda m, mode, method: ([np.array([[0,0],[0,1]])], None))
    res = analyzer.detect_burn_scars(dummy_img)
    burn_mask = res['burn_mask']
    # mask shape should be (1, H, W)
    assert burn_mask.shape == (1, 2, 2)
    # only one pixel is True
    assert int(burn_mask.sum()) == 1
    assert res['burn_area_percentage'] == pytest.approx(1/4)
    assert res['burn_perimeter_length'] == pytest.approx(2.0)


def test_analyze_area(monkeypatch):
    import app.cv.satellite_analyzer as sa
    analyzer = sa.SatelliteAnalyzer(model_path=None)
    monkeypatch.setattr(analyzer, 'analyze_vegetation', lambda img: {'ndvi': 0.5})
    monkeypatch.setattr(analyzer, 'detect_burn_scars', lambda img: {'burn': 10})
    merged = analyzer.analyze_area(np.array([]))
    assert merged == {'ndvi': 0.5, 'burn': 10}


def test_save_and_load_model(tmp_path):
    analyzer = SatelliteAnalyzer(model_path=None)
    path = tmp_path / 'model.pth'
    analyzer.save_model(path)
    assert path.exists() and path.stat().st_size > 0
    # load into new analyzer
    analyzer2 = SatelliteAnalyzer(model_path=None)
    analyzer2.load_model(path)
