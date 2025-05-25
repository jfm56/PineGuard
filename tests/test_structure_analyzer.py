import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from pathlib import Path
from app.risk_analysis.structure_analyzer import StructureAnalyzer


def test_calculate_capacity_risk():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    assert analyzer._analyze_capacity_risk(100, 2) == 1.0
    assert analyzer._analyze_capacity_risk(25, 5) == pytest.approx(0.1)
    assert analyzer._analyze_capacity_risk(0, 0) == 0.0


def test_analyze_amenity_risks():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    assert analyzer._analyze_amenity_risks([]) == 0.0
    val = analyzer._analyze_amenity_risks(['fire_pit', 'grill'])
    assert val == pytest.approx((0.8 + 0.6) / 2)


def test_get_risk_factors():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    site = pd.Series({
        'vegetation_density': 0.8,
        'slope': 16,
        'distance_to_water': 600,
        'cell_coverage': False,
        'distance_to_road': 300
    })
    factors = analyzer._get_risk_factors(site)
    assert 'Dense vegetation' in factors
    assert 'Steep terrain' in factors
    assert 'Limited water access' in factors
    assert 'Poor cell coverage' in factors
    assert 'Remote location' in factors


def test_calculate_congestion_risk():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    roads = gpd.GeoDataFrame({
        'traffic_volume': [50, 100],
        'capacity': [100, 80]
    })
    res = analyzer._calculate_congestion_risk(roads)
    assert list(res) == [0.5, 1.0]


def test_identify_evacuation_routes():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    df = pd.DataFrame({
        'capacity': [10, 20],
        'num_connections': [1, 2],
        'distance_to_highway': [5, 10],
        'congestion_ratio': [0, 0],
        'road_id': ['r1', 'r2'],
        'geometry': [Point(0, 0), Point(1, 1)]
    })
    roads = gpd.GeoDataFrame(df, geometry='geometry')
    routes = analyzer._identify_evacuation_routes(roads)
    assert list(routes['road_id']) == ['r2', 'r1']


def test_calculate_accessibility():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    df = pd.DataFrame({
        'area_id': [1, 1, 2],
        'road_id': ['a', 'b', 'c'],
        'capacity': [10, 20, 30],
        'congestion_ratio': [0.2, 0.5, 0.1]
    })
    roads = gpd.GeoDataFrame(df)
    acc = analyzer._calculate_accessibility(roads)
    assert set(acc.index) == {1, 2}
    assert acc.loc[1, 'num_routes'] == 2
    assert acc.loc[1, 'avg_capacity'] == 15
    assert acc.loc[1, 'avg_congestion'] == pytest.approx(0.35)
    exp = 2 * 0.4 + 15 * 0.4 + (1 - 0.35) * 0.2
    assert acc.loc[1, 'emergency_access_score'] == pytest.approx(exp)


def test_calculate_water_access(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('dummy'))
    buildings = gpd.GeoDataFrame({'geometry': [Point(0, 0)]}, geometry='geometry')
    hydrants = gpd.GeoDataFrame({'geometry': [Point(0, 0)]}, geometry='geometry')
    water_bodies = gpd.GeoDataFrame({'geometry': [Point(0, 0)]}, geometry='geometry')
    def fake_read(path):
        name = Path(path).name
        if name == 'hydrants.geojson':
            return hydrants
        if name == 'water_bodies.geojson':
            return water_bodies
        raise FileNotFoundError
    monkeypatch.setattr(gpd, 'read_file', fake_read)
    wa = analyzer._calculate_water_access(buildings)
    assert wa.iloc[0] == pytest.approx(1.0)


def test_analyze_defensible_space(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('dummy'))
    buildings = gpd.GeoDataFrame({'geometry': [Point(0, 0)]}, geometry='geometry')
    vegetation = gpd.GeoDataFrame({'geometry': [Point(0, 0)], 'density': [0.4]}, geometry='geometry')
    def fake_read(path):
        if Path(path).name == 'vegetation_density.geojson':
            return vegetation
        raise FileNotFoundError
    monkeypatch.setattr(gpd, 'read_file', fake_read)
    ds = analyzer._analyze_defensible_space(buildings)
    assert ds.iloc[0] == pytest.approx(0.6)


def test_analyze_evacuation_routes_file(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('dummy'))
    site = pd.Series({'geometry': Point(0, 0)})
    roads = gpd.GeoDataFrame({
        'road_id': [1],
        'road_type': ['a'],
        'condition': ['good'],
        'is_paved': [True],
        'geometry': [Point(0, 0)]
    }, geometry='geometry')
    def fake_read(path):
        if Path(path).name == 'roads.geojson':
            return roads
        raise FileNotFoundError
    monkeypatch.setattr(gpd, 'read_file', fake_read)
    routes = analyzer._analyze_evacuation_routes(site)
    assert isinstance(routes, list)
    assert routes[0]['road_id'] == 1


def test_analyze_building_vulnerability(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    current_year = pd.Timestamp.now().year
    buildings = gpd.GeoDataFrame({
        'material': ['wood'],
        'year_built': [current_year]
    }, geometry=[Point(0, 0)])
    monkeypatch.setattr(StructureAnalyzer, '_calculate_water_access', lambda self, df: pd.Series([0.8], index=df.index))
    monkeypatch.setattr(StructureAnalyzer, '_analyze_defensible_space', lambda self, df: pd.Series([0.6], index=df.index))
    df = analyzer.analyze_building_vulnerability(buildings)
    assert df.loc[0, 'material_risk'] == 0.9
    assert df.loc[0, 'age_risk'] == 0.0
    assert df.loc[0, 'water_access'] == pytest.approx(0.8)
    assert df.loc[0, 'defensible_space'] == pytest.approx(0.6)
    total = 0.4 * 0.9 + 0.2 * 0.0 + 0.2 * 0.8 + 0.2 * 0.6
    assert df.loc[0, 'total_risk'] == pytest.approx(total)


def test_analyze_camping_areas(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    camping_sites = gpd.GeoDataFrame([{
        'site_id': 's1',
        'capacity': 10,
        'amenities': ['fire_pit']
    }], geometry=[Point(0, 0)])
    monkeypatch.setattr(StructureAnalyzer, '_calculate_base_site_risk', lambda self, site: 0.5)
    monkeypatch.setattr(StructureAnalyzer, '_analyze_evacuation_routes', lambda self, site: [{'route': 'r'}])
    monkeypatch.setattr(StructureAnalyzer, '_analyze_capacity_risk', lambda self, c, n: 0.2)
    monkeypatch.setattr(StructureAnalyzer, '_analyze_amenity_risks', lambda self, a: 0.3)
    monkeypatch.setattr(StructureAnalyzer, '_get_risk_factors', lambda self, site: ['f1', 'f2'])
    df = analyzer.analyze_camping_areas(camping_sites, current_conditions={})
    assert list(df['site_id']) == ['s1']
    score = 0.5 * 0.4 + 0.2 * 0.3 + 0.3 * 0.3
    assert df.loc[0, 'risk_score'] == pytest.approx(score)
    assert df.loc[0, 'evacuation_routes'] == [{'route': 'r'}]
    assert df.loc[0, 'capacity'] == 10
    assert df.loc[0, 'risk_factors'] == ['f1', 'f2']


def test_analyze_area_stub():
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    result = analyzer.analyze_area('foo')
    assert result == {'buildings': [], 'infrastructure': []}


def test_analyze_traffic_patterns(monkeypatch):
    analyzer = StructureAnalyzer(data_dir=Path('.'))
    road_network = gpd.GeoDataFrame({'road_id': [1], 'geometry': [Point(0, 0)]}, geometry='geometry')
    traffic_data = pd.DataFrame({'road_id': [1], 'traffic_volume': [100], 'capacity': [100], 'num_connections': [1], 'distance_to_highway': [1]})
    monkeypatch.setattr(StructureAnalyzer, '_calculate_congestion_risk', lambda self, df: 'c')
    monkeypatch.setattr(StructureAnalyzer, '_identify_evacuation_routes', lambda self, df: 'e')
    monkeypatch.setattr(StructureAnalyzer, '_calculate_accessibility', lambda self, df: 'a')
    res = analyzer.analyze_traffic_patterns(road_network, traffic_data)
    assert res['congestion_risk'] == 'c'
    assert res['evacuation_routes'] == 'e'
    assert res['accessibility_scores'] == 'a'
