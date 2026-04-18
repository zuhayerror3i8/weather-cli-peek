import requests
from .constants import (
    GEO_URL,
    WEATHER_URL
)

def get_coordinates(city):
    """
    Fetches coordinates.
    """
    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(GEO_URL, params=geo_params)

    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            return results[0]
    return None

def get_current(lat, lon, units):
    """
    Fetches current weather data.
    """
    temperature_unit = "celsius" if units == "metric" else "fahrenheit"
    precipitation_unit = "mm" if units == "metric" else "inch"
    wind_speed_unit = "kmh" if units == "metric" else "mph"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "weather_code",
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover",
            "visibility",
            "surface_pressure"
        ],
        "temperature_unit": temperature_unit,
        "precipitation_unit": precipitation_unit,
        "wind_speed_unit": wind_speed_unit,
        "timezone": "auto"
    }

    response = requests.get(WEATHER_URL, params=weather_params)

    if response.status_code == 200:
        data = response.json()
        if "current" in data:
            return data
    return None