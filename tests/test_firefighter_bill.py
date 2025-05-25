import pytest
import app.firefighter_bill as firefighter_bill

def test_firefighter_bill_module_exists():
    assert hasattr(firefighter_bill, "__doc__")

def test_enums_exist():
    from app.firefighter_bill import FuelModelType, VegetationType, WildlifeType, FireRiskLevel
    assert FuelModelType.GR1.value == "Short Grass"
    assert VegetationType.PITCH_PINE.name == "PITCH_PINE"
    assert WildlifeType.BOG_TURTLE.value == "Bog Turtle"
    assert FireRiskLevel.HIGH.value == "High"


def test_weather_conditions_properties():
    from app.firefighter_bill import WeatherConditions
    from datetime import datetime
    time_day = datetime(2025,5,23,12,0)
    time_night = datetime(2025,5,23,2,0)
    sunrise = datetime(2025,5,23,6,0)
    sunset = datetime(2025,5,23,18,0)
    common = {
        "temperature": 70, "humidity": 50, "wind_speed": 3, "wind_direction": "N",
        "wind_gusts": 5, "precipitation": 0, "pressure": 1013, "cloud_cover": 30,
        "cloud_height": 1000, "visibility": 10, "drought_index": 100,
        "fuel_moisture_1h": 5, "fuel_moisture_10h": 7, "fuel_moisture_100h": 10,
        "fuel_moisture_1000h": 15, "mixing_height": 1000, "transport_wind": 5,
        "ventilation_rate": 5000, "sunrise": sunrise, "sunset": sunset
    }
    wc_day = WeatherConditions(timestamp=time_day, **common)
    wc_night = WeatherConditions(timestamp=time_night, **common)
    assert wc_day.is_daytime
    assert not wc_night.is_daytime
    assert wc_day.stability_class == 'A'
    assert wc_night.stability_class == 'F'
    assert not wc_day.red_flag_conditions


def test_infer_and_challenges():
    from app.firefighter_bill import FirefighterBill, VegetationType, FuelModelType
    from app.firefighter_bill import WeatherConditions
    from datetime import datetime
    fb = FirefighterBill()
    # infer fuel types
    types = fb._infer_historical_fuel_types("Bass River State Forest")
    assert isinstance(types, list)
    assert VegetationType.PITCH_PINE in types
    default_types = fb._infer_historical_fuel_types("Unknown")
    assert default_types == [VegetationType.PITCH_PINE, VegetationType.SCRUB_OAK]
    # infer fuel model
    model = fb._infer_historical_fuel_model("Wharton State Forest")
    assert model == FuelModelType.PB_DENSE_PINE
    default_model = fb._infer_historical_fuel_model("Unknown")
    assert default_model == FuelModelType.PB_PINE_SCRUB
    # identify containment challenges
    time = datetime(2025,5,23,12,0)
    sunrise = datetime(2025,5,23,6,0)
    sunset = datetime(2025,5,23,18,0)
    wc = WeatherConditions(
        temperature=70, humidity=20, wind_speed=16, wind_direction="N",
        wind_gusts=0, precipitation=0, pressure=1013, cloud_cover=50,
        cloud_height=1000, visibility=10, drought_index=500,
        fuel_moisture_1h=5, fuel_moisture_10h=7, fuel_moisture_100h=10,
        fuel_moisture_1000h=15, mixing_height=1000, transport_wind=5,
        ventilation_rate=5000, timestamp=time, sunrise=sunrise, sunset=sunset
    )
    challenges = fb._identify_containment_challenges(wc, [VegetationType.PITCH_PINE])
    assert "High winds limiting aerial operations" in challenges
    assert "Low humidity increasing fire intensity" in challenges
    assert "Dense pine fuels with high spotting potential" in challenges
    assert "Severe drought conditions" in challenges
