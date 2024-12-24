import streamlit as st
import requests
from datetime import datetime

class WeatherAgent:
    def __init__(self):
        self.api_key = st.secrets.OPENWEATHER_API_KEY

    def get_weather(self, city, date):
        """
        Fetch weather data from OpenWeather API for a specific city and date.
        """
        # Construct the API URL
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            # Convert the target date to a datetime object
            target_date = datetime.strptime(date, "%Y-%m-%d").date()

            # Loop through the forecast data to find matching dates
            for entry in weather_data["list"]:
                forecast_time = datetime.strptime(
                    entry["dt_txt"], "%Y-%m-%d %H:%M:%S"
                ).date()

                # If the forecast matches the target date, return relevant weather information
                if forecast_time == target_date:
                    weather_description = entry["weather"][0]["description"]
                    temp = entry["main"]["temp"]

                    return {"description": weather_description, "temperature": temp}

            return {"error": "No weather data available for the requested date."}
        else:
            return {"error": "Unable to fetch weather data"}
