import os
import sys
import json
import click
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, api_key):
    """
    Fetches current weather data.
    """
    request_url = f"{BASE_URL}?q={city}&appid={api_key}&units=metric"

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
def main(city):
    """
    Fetches and displays current weather data for a specified CITY.
    """
    load_dotenv()

    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        click.echo("Error: OWM_API_KEY environment variable is missing.")
        sys.exit(1)

    data = get_weather(city, api_key)

    display_weather(data)

if __name__ == "__main__":
    main()