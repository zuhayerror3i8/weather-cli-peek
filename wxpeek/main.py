import sys
import click
from rich.console import Console
from .api import (
    get_coordinates,
    get_current
)
from .display import display_current

console = Console()

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
        data = get_current(location["latitude"], location["longitude"], units)

    if data:
        display_current(location, data, units)
    else:
        console.print("[bright_red]An unexpected error occurred![/]")

if __name__ == "__main__":
    main()