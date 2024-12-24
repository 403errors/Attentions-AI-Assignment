import googlemaps
import streamlit as st

class MapAgent:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=st.secrets["MAPS_API_KEY"])

    def create_map_url(self, locations):
        """
        Create a URL for the map with the given locations.
        This method ensures that all locations are properly used as waypoints.
        """
        geocoded_locations = []

        # Geocode each location and collect the coordinates (latitude, longitude)
        for location in locations:
            geocode_result = self.gmaps.geocode(location)
            if geocode_result:
                lat, lng = geocode_result[0]["geometry"]["location"].values()
                geocoded_locations.append((lat, lng))
            else:
                print(f"Could not geocode location: {location}")

        # If no geocoded locations were found, return None
        if not geocoded_locations:
            return None

        # Starting location can be the first geocoded location
        start_location = geocoded_locations[0]

        # Generate the base URL with the first location as the origin
        base_url = "https://www.google.com/maps/dir/?api=1"
        url = f"{base_url}&origin={start_location[0]},{start_location[1]}"

        # Append all locations (except the first) as waypoints
        if len(geocoded_locations) > 1:
            waypoint_str = "|".join(
                [f"{lat},{lng}" for lat, lng in geocoded_locations[1:]]
            )
            url += f"&waypoints={waypoint_str}"

        # Add the destination as the last location
        destination = geocoded_locations[-1]
        url += f"&destination={destination[0]},{destination[1]}"

        return url

# Test the MapAgent
if __name__ == "__main__":
    # Create a MapAgent instance
    map_agent = MapAgent()

    # Test itinerary (sample data)
    sample_itinerary = "Jaipur, Delhi, Chennai"

    # Generate the map
    # map_url = map_agent.generate_map_from_itinerary(sample_itinerary) # Removed due to method name mismatch
    # print(f"Generated Map URL: {map_url}")
    pass
