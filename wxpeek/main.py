import sys
import click
from rich.console import Console
from .utils import get_coordinates
from .current.api import get_current
from .current.display import display_current
from .hourly.api import get_hourly
from .hourly.display import display_hourly

console = Console()

@click.command()
@click.argument("city", type=str)
@click.option("--units",
              default="metric",
              show_default=True,
              type=click.Choice(["metric", "imperial"]),
              help="Unit system")
@click.option("--hourly",
              is_flag=True,
              help="Show 24-hour forecast")
def main(city, units, hourly):
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
        data = get_current(location["latitude"], location["longitude"], units)
        hourly_data = get_hourly(location["latitude"], location["longitude"], units)

    if data:
        display_current(location, data, units)
    else:
        console.print("[bright_red]An unexpected error occurred![/]")

    if hourly:
        if hourly_data:
            display_hourly(location, hourly_data, units)
        else:
            console.print("[bright_red]An unexpected error occurred![/]")

if __name__ == "__main__":
    main()