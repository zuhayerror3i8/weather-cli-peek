import requests
from .constants import (
    GEO_URL,
    COMPASS
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

def deg_to_compass(degrees):
    return COMPASS[round(degrees / 45) % 8]

def format_visibility(meters, units):
    if units == "metric":
        return f"{meters / 1000:.1f} km"
    return f"{meters / 1609.34:.1f} mi"