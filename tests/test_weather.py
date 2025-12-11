import pytest
from src.weather import get_coordinates, get_weather


def test_get_coordinates_london():
    lat, lon = get_coordinates("London")
    assert lat == pytest.approx(51.5, abs=0.1)
    assert lon == pytest.approx(-0.12, abs=0.1)


def test_get_weather_london():
    weather = get_weather(51.5, -0.12)
    assert isinstance(weather["temperature"], float)
    assert isinstance(weather["windspeed"], float)
    assert isinstance(weather["description"], str)
    assert len(weather["description"]) > 0
