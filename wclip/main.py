import sys
import click
import requests
from rich.console import Console
from rich.table import Table

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Light showers", 81: "Showers", 82: "Heavy showers",
    85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail",
}

COMPASS = [
    "N (North)", "NE (Northeast)",
    "E (East)", "SE (Southeast)",
    "S (South)", "SW (Southwest)",
    "W (West)", "NW (Northwest)",
]

console = Console()

def deg_to_compass(degrees):
    return COMPASS[round(degrees / 45) % 8]

def format_visibility(meters, units):
    if units == "metric":
        return f"{meters / 1000:.1f} km"
    return f"{meters / 1609.34:.1f} mi"

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

def display_weather(data, units):
    """
    Displays current weather data.
    """
    curr = data["current"]
    curr_units = data["current_units"]

    weather_condition = WMO_CODES.get(curr["weather_code"], "Unknown")
    wind_direction = deg_to_compass(curr["wind_direction_10m"])
    visibility = format_visibility(curr["visibility"], units)

    temperature = curr["temperature_2m"]
    apparent_temperature = curr["apparent_temperature"]
    relative_humidity = curr["relative_humidity_2m"]
    precipitation = curr["precipitation"]
    wind_speed = curr["wind_speed_10m"]
    cloud_cover = curr["cloud_cover"]
    surface_pressure = curr["surface_pressure"]

    temperature_unit = curr_units["temperature_2m"]
    apparent_temperature_unit = curr_units["apparent_temperature"]
    relative_humidity_unit = curr_units["relative_humidity_2m"]
    precipitation_unit = curr_units["precipitation"]
    wind_speed_unit = curr_units["wind_speed_10m"]
    cloud_cover_unit = curr_units["cloud_cover"]
    surface_pressure_unit = curr_units["surface_pressure"]

    weather_condition_str = f"{weather_condition}"
    temperature_str = f"{temperature} {temperature_unit}"
    apparent_temperature_str = f"{apparent_temperature} {apparent_temperature_unit}"
    relative_humidity_str = f"{relative_humidity} {relative_humidity_unit}"
    precipitation_str = f"{precipitation} {precipitation_unit}"
    wind_speed_str = f"{wind_speed} {wind_speed_unit}"
    wind_direction_str = f"{wind_direction}"
    cloud_cover_str = f"{cloud_cover} {cloud_cover_unit}"
    visibility_str = f"{visibility}"
    surface_pressure_str = f"{surface_pressure} {surface_pressure_unit}"

    table = Table(show_header=False,
                  box=None,
                  padding=(0, 2))

    table.add_column(style="dim", width=24)
    table.add_column()

    rows = [
        ("Weather Condition", weather_condition_str),
        ("Temperature", temperature_str),
        ("Feels Like", apparent_temperature_str),
        ("Relative Humidity", relative_humidity_str),
        ("Precipitation", precipitation_str),
        ("Wind Speed", wind_speed_str),
        ("Wind Direction", wind_direction_str),
        ("Cloud Cover", cloud_cover_str),
        ("Visibility", visibility_str),
        ("Surface Pressure", surface_pressure_str)
    ]

    for label, value in rows:
        table.add_row(label, value)

    console.print(table)

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