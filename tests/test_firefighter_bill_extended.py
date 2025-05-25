import pytest
from datetime import datetime
from app.firefighter_bill import (
    FirefighterBill,
    WeatherConditions,
    FuelModelType,
    VegetationType,
    WildlifeType,
    FireRiskLevel,
    FireBehaviorPrediction
)


def test_initialize_databases():
    fb = FirefighterBill()
    veg_db = fb.vegetation_database
    wild_db = fb.wildlife_database
    history = fb.historical_fires

    assert isinstance(veg_db, dict)
    assert VegetationType.PITCH_PINE in veg_db

    assert isinstance(wild_db, dict)
    assert WildlifeType.PINE_BARRENS_TREEFROG in wild_db

    assert isinstance(history, list)
    assert history and isinstance(history[0], dict)


def test_enums_values():
    assert FuelModelType.GR1.value == "Short Grass"
    assert VegetationType.SCRUB_OAK.name == "SCRUB_OAK"
    assert WildlifeType.SWAMP_PINK.value == "Swamp Pink"
    assert FireRiskLevel.VERY_HIGH.value == "Very High"


def test_weather_conditions_logic():
    common = {
        "temperature": 70,
        "humidity": 20,
        "wind_speed": 3,
        "wind_direction": "N",
        "wind_gusts": 0,
        "precipitation": 0,
        "pressure": 1013,
        "cloud_cover": 30,
        "cloud_height": 1000,
        "visibility": 10,
        "drought_index": 100,
        "fuel_moisture_1h": 5,
        "fuel_moisture_10h": 7,
        "fuel_moisture_100h": 10,
        "fuel_moisture_1000h": 15,
        "mixing_height": 1000,
        "transport_wind": 5,
        "ventilation_rate": 5000,
        "timestamp": datetime(2025,5,23,12,0),
        "sunrise": datetime(2025,5,23,6,0),
        "sunset": datetime(2025,5,23,18,0)
    }
    wc_day = WeatherConditions(**common)
    wc_night = WeatherConditions(**{**common, "timestamp": datetime(2025,5,23,2,0)})

    # Daytime logic
    assert wc_day.is_daytime
    # Nighttime
    assert not wc_night.is_daytime

    # Stability: wind_speed<5 & cloud_cover<40: 'A' day, 'F' night
    assert wc_day.stability_class == 'A'
    assert wc_night.stability_class == 'F'

    # Red flag: humidity<=25 & wind_speed>=15 & fuel_moisture_10h<=8
    wc_flag = WeatherConditions(**{**common, "humidity": 20, "wind_speed": 15, "fuel_moisture_10h": 8})
    assert wc_flag.red_flag_conditions


def test_calculate_risk_level_various():
    common = {
        "wind_direction": "N",
        "wind_gusts": 0,
        "precipitation": 0,
        "pressure": 1013,
        "cloud_cover": 0,
        "cloud_height": 100,
        "visibility": 10,
        "fuel_moisture_1h": 1,
        "fuel_moisture_10h": 1,
        "fuel_moisture_100h": 1,
        "fuel_moisture_1000h": 1,
        "mixing_height": 100,
        "transport_wind": 1,
        "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0),
        "sunset": datetime(2025,1,1,18,0)
    }
    fb = FirefighterBill()

    # Extreme scenario
    wc_extreme = WeatherConditions(
        temperature=95, humidity=20, wind_speed=25, drought_index=600,
        **common
    )
    assert fb._calculate_risk_level(wc_extreme) == FireRiskLevel.EXTREME

    # Moderate scenario
    wc_mod = WeatherConditions(
        temperature=85, humidity=40, wind_speed=15, drought_index=300,
        **common
    )
    assert fb._calculate_risk_level(wc_mod) == FireRiskLevel.VERY_HIGH

    # Low scenario
    wc_low = WeatherConditions(
        temperature=65, humidity=60, wind_speed=5, drought_index=100,
        **common
    )
    assert fb._calculate_risk_level(wc_low) == FireRiskLevel.LOW


def test_get_firefighting_tactics_behaviors():
    # High risk, high flame
    pred1 = FireBehaviorPrediction(
        risk_level=FireRiskLevel.EXTREME,
        spread_rate=0,
        flame_length=9,
        intensity=0,
        spotting_distance=0,
        containment_challenges=[]
    )
    fb = FirefighterBill()
    tactics1 = fb.get_firefighting_tactics(pred1)
    assert any("escape routes" in t for t in tactics1)
    assert any("Direct attack not recommended" in t for t in tactics1)

    # Low risk, low flame
    pred2 = FireBehaviorPrediction(
        risk_level=FireRiskLevel.LOW,
        spread_rate=0,
        flame_length=3,
        intensity=0,
        spotting_distance=0,
        containment_challenges=[]
    )
    tactics2 = fb.get_firefighting_tactics(pred2)
    assert tactics2 == ["Direct attack with handlines possible"]


def test_predict_fire_behavior_monkeypatched(monkeypatch):
    common = {
        "wind_direction": "N",
        "wind_gusts": 0,
        "precipitation": 0,
        "pressure": 1013,
        "cloud_cover": 0,
        "cloud_height": 100,
        "visibility": 10,
        "fuel_moisture_1h": 1,
        "fuel_moisture_10h": 1,
        "fuel_moisture_100h": 1,
        "fuel_moisture_1000h": 1,
        "mixing_height": 100,
        "transport_wind": 1,
        "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0),
        "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(
        temperature=70, humidity=50, wind_speed=10, drought_index=100,
        **common
    )
    fb = FirefighterBill()
    monkeypatch.setattr(FirefighterBill, '_calculate_risk_level', lambda self, w: FireRiskLevel.MODERATE)
    monkeypatch.setattr(FirefighterBill, '_calculate_spread_rate', lambda self, w, f: 7.0)
    monkeypatch.setattr(FirefighterBill, '_calculate_flame_length', lambda self, sr, f: 5.0)
    monkeypatch.setattr(FirefighterBill, '_calculate_fire_intensity', lambda self, fl: 42.0)
    monkeypatch.setattr(FirefighterBill, '_calculate_spotting_distance', lambda self, w, fl: 1.5)
    monkeypatch.setattr(FirefighterBill, '_identify_containment_challenges', lambda self, w, f: ['X'])

    pred = fb.predict_fire_behavior(wc, [])
    assert pred.risk_level == FireRiskLevel.MODERATE
    assert pred.spread_rate == 7.0
    assert pred.flame_length == 5.0
    assert pred.intensity == 42.0
    assert pred.spotting_distance == 1.5
    assert pred.containment_challenges == ['X']


def test_species_protection_guidelines():
    fb = FirefighterBill()
    spring_guidelines = fb.get_species_protection_guidelines("any", "spring")
    assert "Protect Pine Barrens Treefrog breeding pools" in spring_guidelines
    assert len(spring_guidelines) > 4

    winter_guidelines = fb.get_species_protection_guidelines("any", "winter")
    assert len(winter_guidelines) == 4


def test_infer_historical_fuel_types_and_models():
    fb = FirefighterBill()
    types = fb._infer_historical_fuel_types("Bass River State Forest")
    assert VegetationType.PITCH_PINE in types
    default_types = fb._infer_historical_fuel_types("Unknown")
    assert default_types == [VegetationType.PITCH_PINE, VegetationType.SCRUB_OAK]

    model = fb._infer_historical_fuel_model("Warren Grove Range")
    assert model == FuelModelType.PB_SPARSE_PINE
    default_model = fb._infer_historical_fuel_model("Nowhere")
    assert default_model == FuelModelType.PB_PINE_SCRUB


def test_calculate_spread_rate_simple():
    fb = FirefighterBill()
    common = {
        "temperature": 85, "humidity": 50, "wind_speed": 10,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 0,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    rate = fb._calculate_spread_rate(wc, [])
    assert rate == 4.3


def test_calculate_fire_intensity():
    fb = FirefighterBill()
    intensity = fb._calculate_fire_intensity(0.45)
    assert intensity == 100.0


def test_identify_containment_challenges_all():
    fb = FirefighterBill()
    common = {
        "temperature": 70, "humidity": 25, "wind_speed": 20,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 500,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    challenges = fb._identify_containment_challenges(wc, [VegetationType.PITCH_PINE])
    assert challenges == [
        "High winds limiting aerial operations",
        "Low humidity increasing fire intensity",
        "Dense pine fuels with high spotting potential",
        "Severe drought conditions"
    ]


def test_identify_containment_challenges_none():
    fb = FirefighterBill()
    common = {
        "temperature": 70, "humidity": 60, "wind_speed": 5,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 100,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    none_challenges = fb._identify_containment_challenges(wc, [])
    assert none_challenges == []


def test_fuel_model_and_max_load_and_heat_content():
    fb = FirefighterBill()
    # fuel model loads
    assert fb._get_fuel_model_load(FuelModelType.GR1) == 0.4
    assert fb._get_fuel_model_load(FuelModelType.PB_CEDAR_SWAMP) == 3.5
    # default for unknown
    assert fb._get_fuel_model_load(None) == 1.0
    assert fb._get_max_fuel_load(FuelModelType.GR3) == 2.0
    assert fb._get_max_fuel_load(None) == 3.0
    # heat content
    assert fb._calculate_heat_content([VegetationType.PITCH_PINE]) == 9500
    assert fb._calculate_heat_content([]) == 8000


def test_calculate_terrain_and_spotting_distance_zero():
    fb = FirefighterBill()
    # terrain influence mapping
    assert fb._calculate_terrain_influence("NW") == 1.3
    assert fb._calculate_terrain_influence("unknown") == 1.0
    # spotting distance zero when no wind and zero flame
    common = {
        "temperature": 60, "humidity": 80, "wind_speed": 0,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 0,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    assert fb._calculate_spotting_distance(wc, 0) == 0.0


def test_validate_against_historical_no_recs(monkeypatch):
    fb = FirefighterBill()
    # stub predict_fire_behavior to match historical values for case 0
    pred = FireBehaviorPrediction(
        risk_level=FireRiskLevel.LOW,
        spread_rate=220, flame_length=40,
        intensity=0, spotting_distance=1.2,
        containment_challenges=[]
    )
    monkeypatch.setattr(FirefighterBill, "predict_fire_behavior", lambda self,w,f: pred)
    result = fb.validate_against_historical(0)
    assert result["fire_name"] == "Bass River State Forest Fire (1963)"
    assert result["predicted"]["spread_rate"] == 220
    assert result["actual"]["spread_rate"] == 220
    assert result["differences"]["spread_rate"] == pytest.approx(0)
    assert result["confidence_score"] == 100
    assert result["recommendations"] == []


def test_validate_against_historical_with_recs(monkeypatch):
    fb = FirefighterBill()
    # stub predict_fire_behavior to generate large spread rate diff
    pred = FireBehaviorPrediction(
        risk_level=FireRiskLevel.LOW,
        spread_rate=350, flame_length=40,
        intensity=0, spotting_distance=1.2,
        containment_challenges=[]
    )
    monkeypatch.setattr(FirefighterBill, "predict_fire_behavior", lambda self,w,f: pred)
    result = fb.validate_against_historical(0)
    # confidence should drop below 100
    assert result["confidence_score"] < 100
    # recommendation for spread rate should appear
    assert any("Adjust spread rate calculations for Bass River State Forest" in rec for rec in result["recommendations"])


def test_calculate_flame_length_monkeypatched(monkeypatch):
    fb = FirefighterBill()
    # stub fuel load and heat content to known values
    monkeypatch.setattr(fb, '_calculate_fuel_load', lambda ft: 2.0)
    monkeypatch.setattr(fb, '_calculate_heat_content', lambda ft: 100.0)
    fl = fb._calculate_flame_length(60.0, [VegetationType.PITCH_PINE])
    # intensity = 100 * 2 * (60/60) = 200, L = 0.45 * (200/100)^0.46 ≈ 0.6
    assert fl == pytest.approx(0.6, rel=1e-2)


def test_calculate_spotting_distance_cap():
    fb = FirefighterBill()
    common = {
        "temperature": 100, "humidity": 10, "wind_speed": 30,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 800,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    sd = fb._calculate_spotting_distance(wc, 50)
    # capped at 3 miles
    assert sd == 3.0


def test_calculate_spotting_distance_nonzero():
    fb = FirefighterBill()
    common = {
        "temperature": 90, "humidity": 20, "wind_speed": 15,
        "wind_direction": "NE", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 300,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    sd = fb._calculate_spotting_distance(wc, 10)
    assert 0.0 < sd <= 3.0


def test_calculate_spread_rate_high_wind_precipitation():
    fb = FirefighterBill()
    common = {
        "temperature": 100, "humidity": 20, "wind_speed": 20,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 1,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 100,
        "visibility": 10, "drought_index": 0,
        "fuel_moisture_1h": 0, "fuel_moisture_10h": 0,
        "fuel_moisture_100h": 0, "fuel_moisture_1000h": 0,
        "mixing_height": 100, "transport_wind": 1, "ventilation_rate": 100,
        "timestamp": datetime(2025,1,1,12,0),
        "sunrise": datetime(2025,1,1,6,0), "sunset": datetime(2025,1,1,18,0)
    }
    wc = WeatherConditions(**common)
    rate = fb._calculate_spread_rate(wc, [VegetationType.SCRUB_OAK])
    # Expect wind adjustment and moisture effect branches
    assert rate == pytest.approx(9.2, rel=1e-1)


def test_calculate_fuel_load():
    fb = FirefighterBill()
    # base_load 0.4 + PITCH_PINE adds 2.5
    load = fb._calculate_fuel_load([VegetationType.PITCH_PINE], FuelModelType.GR1)
    assert load == pytest.approx(2.9)
    # base_load 0.7 + PITCH_PINE + SCRUB_OAK adjustments
    load2 = fb._calculate_fuel_load([VegetationType.PITCH_PINE, VegetationType.SCRUB_OAK], FuelModelType.GR3)
    assert load2 == pytest.approx(4.4)


def test_validate_against_historical_flame_and_spot_recs(monkeypatch):
    fb = FirefighterBill()
    # stub predict_fire_behavior to generate large differences for spread, flame, and spotting
    pred = FireBehaviorPrediction(
        risk_level=FireRiskLevel.LOW,
        spread_rate=500, flame_length=100,
        intensity=0, spotting_distance=50,
        containment_challenges=[]
    )
    monkeypatch.setattr(FirefighterBill, "predict_fire_behavior", lambda self,w,f: pred)
    result = fb.validate_against_historical(0)
    recs = result["recommendations"]
    # Expect recommendations for spread rate, flame length, and spotting
    assert any("Adjust spread rate calculations for Bass River State Forest" in r for r in recs)
    assert any("Review fuel load estimates for Bass River State Forest" in r for r in recs)
    assert any("Enhance spotting model for high-wind conditions" in r for r in recs)


def test_stability_and_red_flag_branches():
    common = {
        "temperature": 70, "humidity": 20, "wind_speed": 3,
        "wind_direction": "N", "wind_gusts": 0, "precipitation": 0,
        "pressure": 1013, "cloud_cover": 0, "cloud_height": 1000,
        "visibility": 10, "drought_index": 100,
        "fuel_moisture_1h": 5, "fuel_moisture_10h": 7,
        "fuel_moisture_100h": 10, "fuel_moisture_1000h": 15,
        "mixing_height": 1000, "transport_wind": 5, "ventilation_rate": 5000,
        "timestamp": datetime(2025,5,23,12,0),
        "sunrise": datetime(2025,5,23,6,0), "sunset": datetime(2025,5,23,18,0)
    }
    # Daytime stability branches
    wc = WeatherConditions(**{**common, "wind_speed": 2, "cloud_cover": 30})
    assert wc.stability_class == 'A'
    wc = WeatherConditions(**{**common, "wind_speed": 2, "cloud_cover": 50})
    assert wc.stability_class == 'B'
    wc = WeatherConditions(**{**common, "wind_speed": 2, "cloud_cover": 80})
    assert wc.stability_class == 'C'
    wc = WeatherConditions(**{**common, "wind_speed": 10, "cloud_cover": 30})
    assert wc.stability_class == 'B'
    wc = WeatherConditions(**{**common, "wind_speed": 10, "cloud_cover": 50})
    assert wc.stability_class == 'C'
    wc = WeatherConditions(**{**common, "wind_speed": 10, "cloud_cover": 80})
    assert wc.stability_class == 'D'

    # Nighttime stability branches
    night_common = {**common, "timestamp": datetime(2025,5,23,2,0)}
    wc = WeatherConditions(**{**night_common, "wind_speed": 2, "cloud_cover": 30})
    assert wc.stability_class == 'F'
    wc = WeatherConditions(**{**night_common, "wind_speed": 2, "cloud_cover": 50})
    assert wc.stability_class == 'E'
    wc = WeatherConditions(**{**night_common, "wind_speed": 2, "cloud_cover": 80})
    assert wc.stability_class == 'D'
    wc = WeatherConditions(**{**night_common, "wind_speed": 10, "cloud_cover": 30})
    assert wc.stability_class == 'E'
    wc = WeatherConditions(**{**night_common, "wind_speed": 10, "cloud_cover": 50})
    assert wc.stability_class == 'D'
    wc = WeatherConditions(**{**night_common, "wind_speed": 10, "cloud_cover": 80})
    assert wc.stability_class == 'D'

    # Red flag false scenario
    wc_flag_false = WeatherConditions(**{**common, "humidity": 30, "wind_speed": 15, "fuel_moisture_10h": 8})
    assert not wc_flag_false.red_flag_conditions


def test_get_firefighting_tactics_moderate_cases():
    fb = FirefighterBill()
    # High risk, moderate flame
    pred1 = FireBehaviorPrediction(
        risk_level=FireRiskLevel.HIGH, spread_rate=0,
        flame_length=6, intensity=0, spotting_distance=0,
        containment_challenges=[]
    )
    tactics1 = fb.get_firefighting_tactics(pred1)
    assert tactics1 == ["Use heavy equipment and aerial resources"]

    # High risk, low flame
    pred2 = FireBehaviorPrediction(
        risk_level=FireRiskLevel.HIGH, spread_rate=0,
        flame_length=3, intensity=0, spotting_distance=0,
        containment_challenges=[]
    )
    tactics2 = fb.get_firefighting_tactics(pred2)
    assert tactics2 == ["Direct attack with handlines possible"]
