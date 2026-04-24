from datetime import datetime
import pytz
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..constants import WMO_CODES
from ..colors import (
    color_temperature,
    color_relative_humidity
)

console = Console()

def display_hourly(location, data, units):
    """
    Displays hourly weather data.
    """
    hourly = data["hourly"]
    hourly_units = data["hourly_units"]

    times = hourly["time"]
    weather_conditions = hourly["weather_code"]
    temperatures = hourly["temperature_2m"]
    apparent_temperatures = hourly["apparent_temperature"]
    relative_humidities = hourly["relative_humidity_2m"]

    timezone_str = data["timezone"]
    timezone = pytz.timezone(timezone_str)
    local_time = datetime.now(timezone)
    curr_hour = local_time.strftime("%Y-%m-%dT%H:00")
    curr_idx = times.index(curr_hour)

    times = times[curr_idx:curr_idx + 24]
    weather_conditions = weather_conditions[curr_idx:curr_idx + 24]
    temperatures = temperatures[curr_idx:curr_idx + 24]
    apparent_temperatures = apparent_temperatures[curr_idx:curr_idx + 24]
    relative_humidities = relative_humidities[curr_idx:curr_idx + 24]

    temperature_unit = hourly_units["temperature_2m"]
    apparent_temperature_unit = hourly_units["apparent_temperature"]
    relative_humidity_unit = hourly_units["relative_humidity_2m"]

    table = Table(show_header=True,
                  box=None,
                  padding=(0, 2))

    table.add_column("Time", style="bright_black", width=8, no_wrap=True)
    table.add_column("Weather Cond.", width=16, no_wrap=True)
    table.add_column("Temp.", width=8, no_wrap=True)
    table.add_column("Feels L.", width=10, no_wrap=True)
    table.add_column("R. Humidity", width=12, no_wrap=True)

    neutral_color = "cyan"
    bs_t_c = ""

    for i in range(24):
        time = times[i][11:]
        weather_condition = WMO_CODES.get(weather_conditions[i], "Unknown")
        temperature = temperatures[i]
        apparent_temperature = apparent_temperatures[i]
        relative_humidity = relative_humidities[i]

        temp_celsius = temperature if units == "metric" else (temperature - 32) * 5 / 9
        app_temp_celsius = apparent_temperature if units == "metric" else (apparent_temperature - 32) * 5 / 9

        t_c = color_temperature(temp_celsius)
        bs_t_c = color_temperature(temp_celsius)
        at_c = color_temperature(app_temp_celsius)
        rh_c = color_relative_humidity(relative_humidity)

        time_str = f"{time}"
        weather_condition_str = f"[{neutral_color}]{weather_condition}[/]"
        temperature_str = f"[{t_c}]{temperature} {temperature_unit}[/]"
        apparent_temperature_str = f"[{at_c}]{apparent_temperature} {apparent_temperature_unit}[/]"
        relative_humidity_str = f"[{rh_c}]{relative_humidity} {relative_humidity_unit}[/]"

        table.add_row(
            time_str,
            weather_condition_str,
            temperature_str,
            apparent_temperature_str,
            relative_humidity_str
        )

    panel = Panel(table,
                  title=f"[bold {t_c}]{location['name']}, {location['country']}[/]",
                  subtitle=f"[{t_c}]Powered by Open-Meteo[/]",
                  border_style=bs_t_c,
                  padding=(1, 2),
                  expand=False)

    console.print(panel)