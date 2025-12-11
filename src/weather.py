import urllib.request
import json


def get_coordinates(city: str) -> tuple[float, float]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    result = data["results"][0]
    return (result["latitude"], result["longitude"])
