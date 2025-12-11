import pytest
from unittest.mock import patch
from src.weather import get_coordinates, get_weather, get_forecast, main


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


def test_main_metric(capsys):
    with patch("sys.argv", ["weather", "London"]):
        main()
    captured = capsys.readouterr()
    assert "London:" in captured.out
    assert "°C" in captured.out
    assert "km/h" in captured.out


def test_main_imperial(capsys):
    with patch("sys.argv", ["weather", "London", "--units", "imperial"]):
        main()
    captured = capsys.readouterr()
    assert "London:" in captured.out
    assert "°F" in captured.out
    assert "mph" in captured.out


def test_get_forecast_returns_3_days():
    forecast = get_forecast(51.5, -0.12)
    assert len(forecast) == 3
    for day in forecast:
        assert "date" in day
        assert "temp_max" in day
        assert "temp_min" in day
        assert "description" in day
        assert isinstance(day["temp_max"], float)
        assert isinstance(day["temp_min"], float)


def test_get_forecast_imperial_units():
    metric = get_forecast(51.5, -0.12, units="metric")
    imperial = get_forecast(51.5, -0.12, units="imperial")

    # Imperial temps should be higher (Fahrenheit vs Celsius)
    assert imperial[0]["temp_max"] > metric[0]["temp_max"]


def test_main_forecast(capsys):
    with patch("sys.argv", ["weather", "London", "--forecast"]):
        main()
    captured = capsys.readouterr()
    assert "London" in captured.out
    # Should show 3 days
    lines = [l for l in captured.out.strip().split("\n") if l]
    assert len(lines) >= 3
