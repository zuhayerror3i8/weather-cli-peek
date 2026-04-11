import sys
import click
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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

def color_temperature(celsius):
    if celsius < 0:
        return "bright_cyan"
    if celsius < 15:
        return "bright_blue"
    if celsius < 27:
        return "bright_green"
    if celsius < 35:
        return "bright_yellow"
    return "bright_red"

def color_relative_humidity(percent):
    if percent < 30:
        return "bright_yellow"
    if percent < 60:
        return "bright_green"
    if percent < 80:
        return "bright_cyan"
    return "bright_blue"

def color_wind_speed(kmh):
    if kmh < 10:
        return "bright_green"
    if kmh < 30:
        return "bright_yellow"
    if kmh < 60:
        return "dark_orange"
    return "bright_red"

def color_visibility(km):
    if km < 3:
        return "bright_red"
    if km < 7:
        return "dark_orange"
    if km < 10:
        return "bright_yellow"
    return "bright_green"

def color_cloud_cover(percent):
    if percent < 25:
        return "light_cyan1"
    if percent < 50:
        return "sky_blue1"
    if percent < 75:
        return "deep_sky_blue3"
    return "grey50"

def color_precipitation(mm):
    if mm == 0:
        return "bright_green"
    if mm < 3:
        return "bright_yellow"
    if mm < 10:
        return "dark_orange"
    return "bright_red"

def color_surface_pressure(hpa):
    if hpa < 1000:
        return "bright_red"
    if hpa < 1020:
        return "bright_green"
    return "bright_cyan"

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

def display_weather(location, data, units):
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

    temp_dif_v = temperature if units == "metric" else (temperature - 32) * 5 / 9
    app_temp_dif_v = apparent_temperature if units == "metric" else (apparent_temperature - 32) * 5 / 9
    precip_dif_v = precipitation if units == "metric" else (precipitation * 25.4)
    wind_spd_dif_v = wind_speed if units == "metric" else (wind_speed * 1.60934)
    vis_dif_v = curr["visibility"] / 1000

    t_c = color_temperature(temp_dif_v)
    at_c = color_temperature(app_temp_dif_v)
    rh_c = color_relative_humidity(relative_humidity)
    p_c = color_precipitation(precip_dif_v)
    ws_c = color_wind_speed(wind_spd_dif_v)
    cc_c = color_cloud_cover(cloud_cover)
    v_c = color_visibility(vis_dif_v)
    sp_c = color_surface_pressure(surface_pressure)

    weather_condition_str = f"{weather_condition}"
    temperature_str = f"[{t_c}]{temperature} {temperature_unit}[/]"
    apparent_temperature_str = f"[{at_c}]{apparent_temperature} {apparent_temperature_unit}[/]"
    relative_humidity_str = f"[{rh_c}]{relative_humidity} {relative_humidity_unit}[/]"
    precipitation_str = f"[{p_c}]{precipitation} {precipitation_unit}[/]"
    wind_speed_str = f"[{ws_c}]{wind_speed} {wind_speed_unit}[/]"
    wind_direction_str = f"{wind_direction}"
    cloud_cover_str = f"[{cc_c}]{cloud_cover} {cloud_cover_unit}[/]"
    visibility_str = f"[{v_c}]{visibility}[/]"
    surface_pressure_str = f"[{sp_c}]{surface_pressure} {surface_pressure_unit}[/]"

    table = Table(show_header=False,
                  box=None,
                  padding=(0, 2))

    table.add_column(style="bright_black", width=24)
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

    panel = Panel(table,
                  title=f"[bold {t_c}]{location['name']}, {location['country']}[/]",
                  subtitle=f"[{t_c}]Powered by Open-Meteo[/]",
                  border_style=t_c,
                  padding=(1, 2),
                  expand=False)

    console.print(panel)

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
    with console.status(f"[dark_turquoise]Locating geographic coordinates for [bold cornsilk1]<{city}>...[/]",
                        spinner="point",
                        spinner_style="dark_turquoise"):
        location = get_coordinates(city)

    if not location:
        console.print("[bright_red]Location lookup failed. Please verify spelling or connection![/]")
        sys.exit(1)

    with console.status(f"[dark_turquoise]Fetching meteorological data from [bold cornsilk1]<Open-Meteo>...[/]",
                        spinner="point",
                        spinner_style="dark_turquoise"):
        data = get_weather(location["latitude"], location["longitude"], units)

    if data:
        display_weather(location, data, units)
    else:
        console.print("[bright_red]An unexpected error occurred![/]")

if __name__ == "__main__":
    main()