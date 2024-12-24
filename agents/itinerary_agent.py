from agents.memory_agent import MemoryAgent
from agents.weather_agent import WeatherAgent
from agents.map_agent import MapAgent
from agents.gemini_agent import GeminiAgent
import streamlit as st

# Google API Key for Bard
API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize Agents
memory_agent = MemoryAgent()
gemini_agent = GeminiAgent()

class ItineraryAgent:
    def __init__(self, memory_agent):
        self.memory_agent = memory_agent
        self.weather_agent = WeatherAgent()
        self.map_agent = MapAgent()

    def generate_itinerary(self, city, interests, date_input, starting_point):
        """
        Generate an initial itinerary based on user preferences using Bard.
        """

        # Create the prompt for the model
        prompt = f"""Given the following details about a trip to {city}, generate a creative and detailed itinerary. 
             The user is interested in activities like {', '.join(interests)}.
             The tour starts from {starting_point} on {date_input}.
             Suggest activities such as sightseeing, food, and transportation! Don't make it too long, just the details. 
             And also provide no heder for answering the query."""

        # Generate the itinerary using Bard (Gemini) API
        generated_text = gemini_agent.query(prompt)

        if generated_text:
            return generated_text
        else:
            return "Sorry, I couldn't generate an itinerary at this time."

# Test the ItineraryAgent
if __name__ == "__main__":

    user_preferences = {
        "city": "Delhi",
        "interests": ["history", "food"],
        "budget": 2000,
        "start_time": "9:00 AM",
        "end_time": "6:00 PM",
        "starting_point": "Hotel Roma",
    }

    itinerary_agent = ItineraryAgent(memory_agent)
    itinerary = itinerary_agent.generate_itinerary(user_preferences["city"], user_preferences["interests"], "today", user_preferences["starting_point"])
    # map_url = itinerary_agent.generate_map(itinerary) # Removed due to missing method
    print(f"Generated Itinerary: {itinerary}")
    # print(f"Map URL: {map_url}")
