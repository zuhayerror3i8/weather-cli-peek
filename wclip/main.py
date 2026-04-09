import os
import sys
import json
import click
import requests
from dotenv import load_dotenv
from rich.console import Console

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

console = Console()

def get_weather(city, api_key, units):
    """
    Fetches current weather data.
    """
    request_url = f"{BASE_URL}?q={city}&appid={api_key}&units={units}"

    response = requests.get(request_url)

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
    load_dotenv()

    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        console.print("[red]Error: OWM_API_KEY environment variable is missing.[/red]")
        sys.exit(1)

    data = get_weather(city, api_key, units)

    if data:
        display_weather(data, units)
    else:
        console.print("[red]An unexpected error occurred![/red]")

if __name__ == "__main__":
    main()