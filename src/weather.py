import urllib.request
import json


def get_coordinates(city: str) -> tuple[float, float]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    result = data["results"][0]
    return (result["latitude"], result["longitude"])


WEATHER_CODES: dict[int, str] = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Foggy",
    48: "Foggy",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Light showers",
    81: "Showers",
    82: "Heavy showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather(lat: float, lon: float) -> dict[str, float | str]:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    current = data["current_weather"]
    weather_code = current["weathercode"]
    return {
        "temperature": float(current["temperature"]),
        "windspeed": float(current["windspeed"]),
        "description": WEATHER_CODES.get(weather_code, "Unknown"),
    }
