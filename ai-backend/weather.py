import os
import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(location: str) -> dict:
    """Fetch current weather for `location` from OpenWeatherMap.

    Requires `WEATHER_API_KEY` environment variable to be set.
    Returns the JSON response as a dict. Raises on network/HTTP errors.
    """
    if not API_KEY:
        raise RuntimeError("Missing WEATHER_API_KEY environment variable")

    params = {"q": location, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_weather_history(location: str, days: int = 3) -> list:
    """Fetch historical weather for past N days.
    
    Note: OpenWeatherMap free tier doesn't offer historical data.
    This returns mock data based on current conditions for demo purposes.
    """
    # Get current weather as base
    current = get_weather(location)
    history = []
    
    base_temp = current.get("main", {}).get("temp", 25)
    base_humidity = current.get("main", {}).get("humidity", 50)
    base_wind = current.get("wind", {}).get("speed", 5)
    
    for i in range(days):
        day_offset = days - i
        date = (datetime.datetime.now() - datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")
        temp = base_temp + (i * 0.5)
        humidity = max(30, min(90, base_humidity - (i * 3)))
        wind = base_wind + (i * 0.3)
        
        history.append({
            "date": date,
            "temp": round(temp, 1),
            "humidity": humidity,
            "wind_speed": round(wind, 1),
            "description": "Partly Cloudy" if i == 0 else ("Rainy" if i == 1 else "Clear")
        })
    
    return history
