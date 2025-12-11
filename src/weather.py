import argparse
import urllib.request
import json


LONDON_COORDS = (51.5074, -0.1278)


def get_coordinates(city: str) -> tuple[str, float, float]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        result = data["results"][0]
        return (city, result["latitude"], result["longitude"])
    except (KeyError, IndexError, urllib.error.URLError):
        return ("London", *LONDON_COORDS)


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Get weather for a city")
    parser.add_argument("city", help="City name")
    args = parser.parse_args()

    city, lat, lon = get_coordinates(args.city)
    weather = get_weather(lat, lon)
    print(f"{city}: {weather['temperature']}°C, {weather['description']}, Wind: {weather['windspeed']} km/h")


if __name__ == "__main__":
    main()
