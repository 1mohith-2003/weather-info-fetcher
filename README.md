# Weather Information Fetcher

A simple Python + Streamlit app that fetches current weather and a 7-day forecast using the Open-Meteo API (no API key required). Includes basic geocoding using Nominatim (OpenStreetMap).

## Files
- `streamlit_app.py` — main Streamlit app
- `weather.py` — API client for Open-Meteo and Nominatim
- `requirements.txt` — Python dependencies
- `.gitignore`

## How to run locally
1. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
