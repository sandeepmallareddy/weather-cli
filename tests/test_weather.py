import pytest
from src.weather import get_coordinates


def test_get_coordinates_london():
    lat, lon = get_coordinates("London")
    assert lat == pytest.approx(51.5, abs=0.1)
    assert lon == pytest.approx(-0.12, abs=0.1)
