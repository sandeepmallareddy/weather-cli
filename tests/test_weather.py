import pytest
from src.weather import get_coordinates, get_weather


def test_get_coordinates_london():
    city, lat, lon = get_coordinates("London")
    assert city == "London"
    assert lat == pytest.approx(51.5, abs=0.1)
    assert lon == pytest.approx(-0.12, abs=0.1)


def test_get_coordinates_invalid_city():
    with pytest.raises(ValueError, match="City not found"):
        get_coordinates("FakeCityXYZ123")


def test_get_weather_london():
    weather = get_weather(51.5, -0.12)
    assert isinstance(weather["temperature"], float)
    assert isinstance(weather["windspeed"], float)
    assert isinstance(weather["description"], str)
    assert len(weather["description"]) > 0


def test_get_weather_imperial_units():
    weather = get_weather(51.5, -0.12, units="imperial")
    assert isinstance(weather["temperature"], float)
    assert isinstance(weather["windspeed"], float)
    assert isinstance(weather["description"], str)


def test_units_conversion():
    metric = get_weather(51.5, -0.12, units="metric")
    imperial = get_weather(51.5, -0.12, units="imperial")

    expected_temp_f = metric["temperature"] * 9 / 5 + 32
    expected_wind_mph = metric["windspeed"] * 0.621371

    assert imperial["temperature"] == pytest.approx(expected_temp_f, abs=0.2)
    assert imperial["windspeed"] == pytest.approx(expected_wind_mph, abs=0.1)
