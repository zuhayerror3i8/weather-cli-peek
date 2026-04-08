import os
import sys
import json
import click
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@click.command()
@click.argument("city", type=str)
def weather(city):
    """
    Fetches and displays current weather data for a specified CITY.
    """
    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        click.echo("Error: OWM_API_KEY environment variable is missing.")
        sys.exit(1)

    request_url = f"{BASE_URL}?q={city}&appid={api_key}&units=metric"

    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo("An unexpected error occurred!")

if __name__ == "__main__":
    weather()