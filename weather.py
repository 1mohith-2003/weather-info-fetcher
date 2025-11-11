# weather.py
import requests

class WeatherClient:
    """
    Simple client for Open-Meteo (no API key) and Nominatim geocoding.
    """

    def __init__(self):
        self.meteo_url = "https://api.open-meteo.com/v1/forecast"
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"

    def geocode(self, place_name, limit=1):
        """
        Resolve a place name to (lat, lon) using Nominatim.
        Returns (lat, lon) as floats or None.
        """
        params = {
            "q": place_name,
            "format": "json",
            "limit": limit
        }
        try:
            resp = requests.get(self.nominatim_url, params=params, headers={"User-Agent":"weather-info-fetcher/1.0"})
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return None
            entry = data[0]
            return float(entry["lat"]), float(entry["lon"])
        except Exception:
            return None

    def human_location(self, lat, lon):
        return f"{lat:.4f}, {lon:.4f}"

    def get_weather(self, lat, lon):
        """
        Query Open-Meteo for current weather and daily forecast.
        Returns parsed JSON or None.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto"
        }
        try:
            resp = requests.get(self.meteo_url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None
