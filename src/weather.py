import argparse
import urllib.request
import json


def get_coordinates(city: str) -> tuple[str, float, float]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        result = data["results"][0]
        return (city, result["latitude"], result["longitude"])
    except (KeyError, IndexError):
        raise ValueError(f"City not found: {city}")


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


def get_weather(lat: float, lon: float, units: str = "metric") -> dict[str, float | str]:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    current = data["current_weather"]
    weather_code = current["weathercode"]

    temperature = float(current["temperature"])
    windspeed = float(current["windspeed"])

    if units == "imperial":
        temperature = temperature * 9 / 5 + 32
        windspeed = windspeed * 0.621371

    return {
        "temperature": round(temperature, 1),
        "windspeed": round(windspeed, 1),
        "description": WEATHER_CODES.get(weather_code, "Unknown"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Get weather for a city")
    parser.add_argument("city", help="City name")
    parser.add_argument("--units", choices=["metric", "imperial"], default="metric",
                        help="Unit system (default: metric)")
    args = parser.parse_args()

    city, lat, lon = get_coordinates(args.city)
    weather = get_weather(lat, lon, args.units)

    if args.units == "imperial":
        temp_unit = "°F"
        wind_unit = "mph"
    else:
        temp_unit = "°C"
        wind_unit = "km/h"

    print(f"{city}: {weather['temperature']}{temp_unit}, {weather['description']}, Wind: {weather['windspeed']} {wind_unit}")


if __name__ == "__main__":
    main()
