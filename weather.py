# weather.py

import requests

API_KEY = "96808bbc5c1b7bc81a7d665696a5bfe2"

def get_data(place, forecast_days=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "list" not in data:
        return []  # Return empty list if no valid forecast found

    filtered_data = data["list"]
    nr_values = 8 * forecast_days  # 3-hour interval, 8 per day
    return filtered_data[:nr_values]
