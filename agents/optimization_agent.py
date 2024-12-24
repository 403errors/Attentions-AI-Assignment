import googlemaps
import toml
import spacy
from datetime import datetime
from dotenv import load_dotenv
secrets = toml.load("secrets.toml")

from agents.memory_agent import MemoryAgent
from agents.gemini_agent import GeminiAgent

# Load environment variables
load_dotenv()

# Initialize agents
memory_agent = MemoryAgent()
gemini_agent = GeminiAgent()


# OptimizationAgent class
class OptimizationAgent:
    def __init__(self, memory_agent):
        self.memory_agent = memory_agent
        self.gmaps = googlemaps.Client(key=secrets["MAPS_API_KEY"])
        self.nlp = spacy.load("en_core_web_sm")

    def locations_from_itinerary(self, itinerary):
        # Process the input text with spaCy
        doc = self.nlp(itinerary)

        # Extract named entities that are places
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        return locations

    def optimize_path(self, itinerary, budget, start_time, end_time):
        """
        Optimizes the given itinerary based on budget and time constraints.

        inputs - itinerary, budget, start_time, end_time
        """
        prompt = f"""
        You are an expert travel planner specializing in single-day itineraries. Your task is to optimize the provided itinerary to ensure it fits within the user's constraints for the specified date. 

        Details:
        - Itinerary: {itinerary}
        - Date: {start_time.date().strftime("%Y-%m-%d")}  # This will now work correctly
        - Budget: INR {budget}
        - Start Time: {start_time.strftime("%H:%M")}
        - End Time: {end_time.strftime("%H:%M")}
        - Total available time: {(end_time - start_time).seconds // 3600} hours
        """

        # Example call to a language model for optimization
        optimized_itinerary = gemini_agent.query(prompt)
        return optimized_itinerary

    def get_geocoded_locations(self, itinerary):
        """
        Get geocoded locations (lat, lng) for each place in the itinerary.
        """
        if itinerary:
            places = self.locations_from_itinerary(
                itinerary
            )  # Use the extracted places

            # Geocode these places using Google Maps API
            geocoded_places = []
            for place in places:
                geocode_result = self.gmaps.geocode(place)
                if geocode_result:
                    lat_lng = geocode_result[0]["geometry"]["location"]
                    geocoded_places.append((place, lat_lng["lat"], lat_lng["lng"]))
                else:
                    print(f"Could not geocode place: {place}")
            return geocoded_places
        else:
            return "Sorry, I couldn't fetch places from itinerary."


# Example usage
if __name__ == "__main__":
    # Sample itinerary (can be replaced with dynamic input)
    itinerary = [
        "Colosseum, Rome",
        "Vatican Museum, Rome",
        "Roman Forum, Rome",
        "Pantheon, Rome",
    ]

    # Example max time constraint (in minutes)
    budget = 10000  # INR
    start_time = datetime(2024, 11, 30, 9, 0)  # 9:00 AM on the given date
    end_time = datetime(2024, 11, 30, 18, 0)  # 6:00 PM on the given date

    # Create an instance of OptimizationAgent
    optimization_agent = OptimizationAgent(
        memory_agent
    )  # Pass in the memory_agent instance

    # Call the optimize_path method with the correct parameters
    optimized_itinerary = optimization_agent.optimize_path(
        itinerary, budget, start_time, end_time
    )

    # Print the optimized itinerary
    print("Optimized Itinerary:", optimized_itinerary)
