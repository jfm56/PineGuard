import datetime
import pytest

from app.firefighter_bill import WeatherConditions, FirefighterBill, VegetationType, FuelModelType

# Helper to create a basic WeatherConditions instance
def make_weather(
    wind_speed=0.0,
    humidity=50.0,
    fuel_moisture_10h=10.0,
    wind_direction="N",
    timestamp=None,
    sunrise=None,
    sunset=None,
):
    now = timestamp or datetime.datetime(2021, 6, 1, 12, 0)
    sr = sunrise or datetime.datetime(2021, 6, 1, 6, 0)
    ss = sunset or datetime.datetime(2021, 6, 1, 18, 0)
    return WeatherConditions(
        temperature=70.0,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        wind_gusts=0.0,
        precipitation=0.0,
        pressure=1013.0,
        cloud_cover=0,
        cloud_height=1000.0,
        visibility=10.0,
        drought_index=300,
        fuel_moisture_1h=10.0,
        fuel_moisture_10h=fuel_moisture_10h,
        fuel_moisture_100h=15.0,
        fuel_moisture_1000h=20.0,
        mixing_height=500.0,
        transport_wind=5.0,
        ventilation_rate=500.0 * 5.0,
        timestamp=now,
        sunrise=sr,
        sunset=ss,
    )

# WeatherConditions properties
def test_is_daytime_true():
    w = make_weather()
    assert w.is_daytime is True


def test_is_daytime_false():
    ts = datetime.datetime(2021, 6, 1, 5, 0)
    w = make_weather(timestamp=ts)
    assert w.is_daytime is False


def test_stability_class_various():
    # Daytime low wind, low cloud -> A
    w = make_weather(wind_speed=3, humidity=50.0)
    w.cloud_cover = 20
    assert w.stability_class == 'A'
    # Nighttime low wind, low cloud -> F
    w2 = make_weather(wind_speed=3)
    w2.cloud_cover = 20
    w2.timestamp = datetime.datetime(2021,6,1,23,0)
    assert w2.stability_class == 'F'
    # Moderate wind -> D
    w3 = make_weather(wind_speed=8)
    w3.cloud_cover = 80
    assert w3.stability_class == 'D'


def test_red_flag_conditions_true_and_false():
    # True when wind>=15, humidity<=25, fuel_moisture_10h<=8
    w = make_weather(wind_speed=15, humidity=25, fuel_moisture_10h=8)
    assert w.red_flag_conditions is True
    # False otherwise
    w2 = make_weather(wind_speed=10, humidity=30, fuel_moisture_10h=10)
    assert w2.red_flag_conditions is False

# FirefighterBill infer methods
def test_infer_historical_fuel_types_known_and_default():
    bill = FirefighterBill()
    types = bill._infer_historical_fuel_types("Warren Grove Range")
    assert VegetationType.PITCH_PINE in types
    # Default fallback
    types2 = bill._infer_historical_fuel_types("Unknown Location")
    assert types2 == [VegetationType.PITCH_PINE, VegetationType.SCRUB_OAK]


def test_infer_historical_fuel_model_known_and_default():
    bill = FirefighterBill()
    model = bill._infer_historical_fuel_model("Wharton State Forest")
    assert model == FuelModelType.PB_DENSE_PINE
    model2 = bill._infer_historical_fuel_model("Nowhere")
    assert model2 == FuelModelType.PB_PINE_SCRUB


def test_identify_containment_challenges():
    bill = FirefighterBill()
    # High wind and low humidity and drought and pitch pine
    w = make_weather(wind_speed=20, humidity=20, fuel_moisture_10h=10)
    w.drought_index = 500
    challenges = bill._identify_containment_challenges(w, [VegetationType.PITCH_PINE])
    assert "High winds limiting aerial operations" in challenges
    assert "Low humidity increasing fire intensity" in challenges
    assert "Dense pine fuels with high spotting potential" in challenges
    assert "Severe drought conditions" in challenges
    # No challenges
    w2 = make_weather(wind_speed=1, humidity=50)
    w2.drought_index = 100
    challenges2 = bill._identify_containment_challenges(w2, [])
    assert challenges2 == []


def test_get_species_protection_guidelines():
    bill = FirefighterBill()
    # Spring season
    guides = bill.get_species_protection_guidelines("Any", "Spring")
    assert "Protect Pine Barrens Treefrog breeding pools" in guides
    # Other season
    guides2 = bill.get_species_protection_guidelines("Any", "Fall")
    assert all("Protect Pine Barrens Treefrog" not in g for g in guides2)
