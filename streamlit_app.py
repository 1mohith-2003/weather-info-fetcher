# streamlit_app.py
import streamlit as st
from weather import WeatherClient
from datetime import datetime

st.set_page_config(page_title="Weather Info Fetcher", layout="centered")

st.title("🌤️ Weather Information Fetcher")
st.write("Fetch current weather and 7-day forecast using the Open-Meteo API (no API key required).")

# Input
col1, col2 = st.columns([3,1])
with col1:
    place = st.text_input("Enter a city or latitude,longitude (e.g. 'New Delhi' or '28.6139,77.2090')", value="New Delhi")
with col2:
    units = st.selectbox("Units", ["metric (°C)", "imperial (°F)"])

# Helper
def parse_latlon(text):
    # if user enters "lat,lon"
    if "," in text:
        try:
            lat_str, lon_str = [s.strip() for s in text.split(",", 1)]
            return float(lat_str), float(lon_str)
        except Exception:
            return None
    return None

# Fetch on button
if st.button("Get Weather"):
    coords = parse_latlon(place)
    client = WeatherClient()

    with st.spinner("Resolving location and fetching weather..."):
        if coords:
            lat, lon = coords
        else:
            # geocode city name (simple, uses Nominatim)
            latlon = client.geocode(place)
            if not latlon:
                st.error("Could not resolve location. Try 'latitude,longitude' or another place name.")
                st.stop()
            lat, lon = latlon

        # Get weather
        data = client.get_weather(lat, lon)
        if not data:
            st.error("Weather API request failed. Try again later.")
            st.stop()

    # Display header
    st.markdown(f"### Location: {client.human_location(lat, lon)}")
    st.markdown(f"**Coordinates:** {lat:.4f}, {lon:.4f}")

    # Current weather
    current = data.get("current_weather", {})
    if current:
        temp_c = current.get("temperature")
        windspeed = current.get("windspeed")
        weather_time = current.get("time")
        st.subheader("Current Weather")
        if "metric" in units:
            st.write(f"Temperature: **{temp_c} °C**")
        else:
            # convert C -> F
            temp_f = temp_c * 9/5 + 32
            st.write(f"Temperature: **{temp_f:.1f} °F**")
        st.write(f"Wind speed: **{windspeed} m/s**")
        st.write(f"Observation time: {weather_time}")

    # Daily forecast
    daily = data.get("daily", {})
    if daily:
        st.subheader("7-day Forecast")
        days = daily.get("time", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        table_rows = []
        for d, tmax, tmin in zip(days, temps_max, temps_min):
            dt = datetime.fromisoformat(d).strftime("%a, %d %b %Y")
            if "metric" in units:
                row = (dt, f"{tmax} °C", f"{tmin} °C")
            else:
                row = (dt, f"{tmax * 9/5 + 32:.1f} °F", f"{tmin * 9/5 + 32:.1f} °F")
            table_rows.append(row)

        st.table({"Day": [r[0] for r in table_rows],
                  "Max": [r[1] for r in table_rows],
                  "Min": [r[2] for r in table_rows]})
