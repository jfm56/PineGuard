import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
from app.risk_analysis.fuel_analyzer import FuelAnalyzer


def test_init_default():
    fa = FuelAnalyzer()
    assert isinstance(fa.fuel_types, pd.DataFrame)
    assert fa.fuel_types.empty


def test_calculate_dead_fuel_moisture():
    fa = FuelAnalyzer()
    res = fa._calculate_dead_fuel_moisture(20.0, 50.0, 0.1)
    basic = 0.03 * 50.0 - 0.14 * 20.0 + 21.0 * 0.1 + 20
    assert res['1_hour'] == pytest.approx(basic * 0.8)
    assert res['10_hour'] == pytest.approx(basic * 1.0)
    assert res['100_hour'] == pytest.approx(basic * 1.2)


def test_calculate_live_fuel_moisture_with_ndvi():
    fa = FuelAnalyzer()
    veg = gpd.GeoDataFrame({'ndvi': [0.5, 0.7]}, geometry=[Point(0,0), Point(1,1)])
    res = fa._calculate_live_fuel_moisture(veg)
    mean = veg['ndvi'].mean()
    assert res['woody'] == pytest.approx(mean * 200)
    assert res['herbaceous'] == pytest.approx(mean * 300)


def test_calculate_live_fuel_moisture_default():
    fa = FuelAnalyzer()
    veg = gpd.GeoDataFrame({'other': [1]}, geometry=[Point(0,0)])
    res = fa._calculate_live_fuel_moisture(veg)
    assert res == {'woody': 100, 'herbaceous': 150}


def test_calculate_drought_index():
    fa = FuelAnalyzer()
    wd = pd.DataFrame({'precipitation': [1, 1], 'temperature': [10, 10]})
    val = fa._calculate_drought_index(wd)
    expected = (800 - 2 * 100 + 10 * 2) / 800
    assert val == pytest.approx(expected)


def test_determine_season_characteristics():
    fa = FuelAnalyzer()
    spring = fa._determine_season_characteristics(pd.Timestamp('2025-04-01'))
    assert spring['season'] == 'spring'
    assert spring['is_fire_season']
    winter = fa._determine_season_characteristics(pd.Timestamp('2025-01-15'))
    assert winter['season'] == 'winter'
    assert not winter['is_fire_season']


def test_calculate_curing_level():
    fa = FuelAnalyzer()
    wd = pd.DataFrame({'temperature': [30, 30], 'precipitation': [0, 0]})
    val = fa._calculate_curing_level('summer', wd)
    assert val == pytest.approx(0.6)


def test_generate_recommendations():
    fa = FuelAnalyzer()
    rec = fa._generate_recommendations(0.9)
    assert 'Immediate fuel reduction required' in rec
    rec2 = fa._generate_recommendations(0.7)
    assert 'Regular fuel management needed' in rec2
    rec3 = fa._generate_recommendations(0.5)
    assert 'Continue routine maintenance' in rec3


def test_calculate_fuel_load(monkeypatch):
    fa = FuelAnalyzer()
    # stub surface and canopy
    monkeypatch.setattr(FuelAnalyzer, '_calculate_surface_fuel_load', lambda self, a: {'total': 5})
    monkeypatch.setattr(FuelAnalyzer, '_calculate_canopy_fuel_load', lambda self, a: {'total': 10})
    # area with forest
    area = gpd.GeoDataFrame({'vegetation_type': ['forest']}, geometry=[Point(0,0)])
    fl = fa._calculate_fuel_load(area)
    assert fl['surface_fuel'] == 5
    assert fl['canopy_fuel'] == 10
    assert fl['total_fuel'] == 15
    # area without forest
    area2 = gpd.GeoDataFrame({'vegetation_type': ['grass']}, geometry=[Point(0,0)])
    fl2 = fa._calculate_fuel_load(area2)
    assert fl2['surface_fuel'] == 5
    assert fl2['canopy_fuel'] == 0
    assert fl2['total_fuel'] == 5


def test_calculate_fuel_characteristics(monkeypatch):
    fa = FuelAnalyzer()
    # stub distribution etc.
    dist = pd.Series([0.8, 0.2], index=['type1','type2'])
    monkeypatch.setattr(FuelAnalyzer, '_analyze_fuel_distribution', lambda self, a: dist)
    monkeypatch.setattr(FuelAnalyzer, '_calculate_horizontal_continuity', lambda self, a: 0.5)
    monkeypatch.setattr(FuelAnalyzer, '_calculate_vertical_continuity', lambda self, a: 0.4)
    monkeypatch.setattr(FuelAnalyzer, '_analyze_fuel_depth', lambda self, a: 1.2)
    area = gpd.GeoDataFrame({}, geometry=[Point(0,0)])
    out = fa._calculate_fuel_characteristics(area)
    assert out['fuel_distribution'] is dist
    assert out['horizontal_continuity'] == 0.5
    assert out['vertical_continuity'] == 0.4
    assert out['fuel_depth'] == 1.2
    assert out['primary_fuel_type'] == 'type1'


def test_analyze_fuel_hazards(monkeypatch):
    fa = FuelAnalyzer()
    # stub internals
    monkeypatch.setattr(FuelAnalyzer, '_calculate_fuel_characteristics', lambda self, a: {'fc': 1})
    monkeypatch.setattr(FuelAnalyzer, '_analyze_fuel_moisture', lambda self, a, b, c: {'mo': 2})
    monkeypatch.setattr(FuelAnalyzer, '_calculate_fuel_load', lambda self, a: {'fl': 3})
    monkeypatch.setattr(FuelAnalyzer, '_analyze_seasonal_effects', lambda self, b, d: {'sf': 4})
    monkeypatch.setattr(FuelAnalyzer, '_calculate_hazard_score', lambda self, a, b, c, d: 0.75)
    monkeypatch.setattr(FuelAnalyzer, '_generate_recommendations', lambda self, h: ['ok'])
    area = gpd.GeoDataFrame({}, geometry=[Point(0,0)])
    wd = pd.DataFrame()
    vd = None
    res = fa.analyze_fuel_hazards(area, wd, vd)
    assert res['hazard_score'] == 0.75
    assert res['fuel_characteristics'] == {'fc': 1}
    assert res['moisture_content'] == {'mo': 2}
    assert res['fuel_load'] == {'fl': 3}
    assert res['seasonal_factors'] == {'sf': 4}
    assert res['recommendations'] == ['ok']


def test_analyze_area_stub():
    fa = FuelAnalyzer()
    assert fa.analyze_area('x') == {'fuel_type': None, 'fuel_moisture': None}
