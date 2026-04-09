import os
import sys
import json
import click
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, api_key, units):
    """
    Fetches current weather data.
    """
    request_url = f"{BASE_URL}?q={city}&appid={api_key}&units={units}"

    response = requests.get(request_url)

    if response.status_code == 200:
        return response.json()
    return None

def display_weather(data):
    """
    Displays current weather data.
    """
    if data:
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo("An unexpected error occurred!")

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
        click.echo("Error: OWM_API_KEY environment variable is missing.")
        sys.exit(1)

    data = get_weather(city, api_key, units)

    display_weather(data)

if __name__ == "__main__":
    main()