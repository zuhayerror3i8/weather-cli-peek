from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..constants import WMO_CODES
from ..utils import (
    deg_to_compass,
    format_visibility
)
from ..colors import (
    color_temperature,
    color_relative_humidity,
    color_precipitation,
    color_wind_speed,
    color_cloud_cover,
    color_visibility,
    color_surface_pressure,
)

console = Console()

def display_current(location, data, units):
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

    temp_celsius = temperature if units == "metric" else (temperature - 32) * 5 / 9
    app_temp_celsius = apparent_temperature if units == "metric" else (apparent_temperature - 32) * 5 / 9
    precip_mm = precipitation if units == "metric" else (precipitation * 25.4)
    wind_spd_kmh = wind_speed if units == "metric" else (wind_speed * 1.60934)
    vis_km = curr["visibility"] / 1000

    neutral_color = "cyan"
    t_c = color_temperature(temp_celsius)
    at_c = color_temperature(app_temp_celsius)
    rh_c = color_relative_humidity(relative_humidity)
    p_c = color_precipitation(precip_mm)
    ws_c = color_wind_speed(wind_spd_kmh)
    cc_c = color_cloud_cover(cloud_cover)
    v_c = color_visibility(vis_km)
    sp_c = color_surface_pressure(surface_pressure)

    weather_condition_str = f"[{neutral_color}]{weather_condition}[/]"
    temperature_str = f"[{t_c}]{temperature} {temperature_unit}[/]"
    apparent_temperature_str = f"[{at_c}]{apparent_temperature} {apparent_temperature_unit}[/]"
    relative_humidity_str = f"[{rh_c}]{relative_humidity} {relative_humidity_unit}[/]"
    precipitation_str = f"[{p_c}]{precipitation} {precipitation_unit}[/]"
    wind_speed_str = f"[{ws_c}]{wind_speed} {wind_speed_unit}[/]"
    wind_direction_str = f"[{neutral_color}]{wind_direction}[/]"
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