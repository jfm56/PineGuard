import pytest
from datetime import datetime
from fastapi import HTTPException
from app.api import map_data


def test_calculate_risk_areas():
    areas = map_data.calculate_risk_areas()
    assert isinstance(areas, list)
    assert len(areas) == 4

    # High risk area
    first = areas[0]
    assert first['riskLevel'] == 'High'
    assert first['coords'] == [39.7825, -74.5338]
    assert first['severity'] == 2.5
    assert any(f['name']=='Vegetation Dryness' and f['value']=='Critical' for f in first['factors'])

    # Moderate risk area
    third = areas[2]
    assert third['riskLevel'] == 'Moderate'
    assert third['severity'] == 1.5
    assert any(f['name']=='Wind Speed' and f['value']=='Moderate' for f in third['factors'])


@pytest.mark.asyncio
async def test_get_map_data_success():
    result = await map_data.get_map_data()
    assert result['fireStations'] == map_data.FIRE_STATIONS
    assert result['waterSources'] == map_data.WATER_SOURCES
    assert result['evacuationRoutes'] == map_data.EVACUATION_ROUTES
    assert result['bounds'] == map_data.PINE_BARRENS['bounds']


@pytest.mark.asyncio
async def test_get_map_data_exception(monkeypatch):
    monkeypatch.setattr(map_data, 'PINE_BARRENS', {})
    with pytest.raises(HTTPException) as excinfo:
        await map_data.get_map_data()
    assert excinfo.value.status_code == 500
    assert 'bounds' in excinfo.value.detail


@pytest.mark.asyncio
async def test_get_fire_risk_current():
    result = await map_data.get_fire_risk()
    assert result['timeRange'] == 'current'
    assert isinstance(result['timestamp'], str)
    datetime.fromisoformat(result['timestamp'])
    assert isinstance(result['riskAreas'], list)
    assert len(result['riskAreas']) == 4


@pytest.mark.asyncio
async def test_get_fire_risk_24h():
    result = await map_data.get_fire_risk('24h')
    assert result['timeRange'] == '24h'
    assert len(result['riskAreas']) == 5
    last = result['riskAreas'][-1]
    assert last['riskLevel'] == 'High'
    assert any(f['name']=='Wind Forecast' and f['value']=='Increasing' for f in last['factors'])


@pytest.mark.asyncio
async def test_get_fire_risk_week():
    result = await map_data.get_fire_risk('week')
    assert result['timeRange'] == 'week'
    assert len(result['riskAreas']) == 5
    last = result['riskAreas'][-1]
    assert last['riskLevel'] == 'Moderate'
    assert any(f['name']=='Seasonal Trend' and f['value']=='Above Average' for f in last['factors'])


@pytest.mark.asyncio
async def test_get_fire_risk_exception(monkeypatch):
    def raise_error():
        raise ValueError('test failure')
    monkeypatch.setattr(map_data, 'calculate_risk_areas', raise_error)
    with pytest.raises(HTTPException) as excinfo:
        await map_data.get_fire_risk()
    assert excinfo.value.status_code == 500
    assert 'test failure' in excinfo.value.detail
