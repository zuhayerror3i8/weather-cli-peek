import requests
from ..constants import WEATHER_URL

def get_hourly(lat, lon, units):
    """
    Fetches hourly weather data.
    """
    temperature_unit = "celsius" if units == "metric" else "fahrenheit"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "weather_code",
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m"
        ],
        "temperature_unit": temperature_unit,
        "timezone": "auto"
    }

    response = requests.get(WEATHER_URL, params=weather_params)

    if response.status_code == 200:
        data = response.json()
        if "hourly" in data:
            return data
    return None