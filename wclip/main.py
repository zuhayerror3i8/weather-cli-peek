import sys
import json
import click
import requests
from rich.console import Console

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

console = Console()

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

def get_weather(lat, lon, units):
    """
    Fetches current weather data.
    """
    temperature_unit = "celsius" if units == "metric" else "fahrenheit"
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
        "wind_speed_unit": wind_speed_unit,
        "timezone": "auto"
    }

    response = requests.get(WEATHER_URL, params=weather_params)

    if response.status_code == 200:
        return response.json()
    return None

def display_weather(data, units):
    """
    Displays current weather data.
    """
    console.print(json.dumps(data, indent=2))

@click.command()
@click.argument("city", type=str)
@click.option("--units",
              default="metric",
              show_default=True,
              type=click.Choice(["metric", "imperial"]),
              help="Unit system")
def main(city, units):
    """
    Fetches and displays current weather data for a specified CITY.
    """
    location = get_coordinates(city)

    if not location:
        console.print("[red]Location lookup failed. Please verify spelling or connection![/red]")
        sys.exit(1)

    data = get_weather(location["latitude"], location["longitude"], units)

    if data:
        display_weather(data, units)
    else:
        console.print("[red]An unexpected error occurred![/red]")

if __name__ == "__main__":
    main()