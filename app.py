import streamlit as st
import os
from datetime import datetime
from agents.map_agent import MapAgent
from agents.user_interaction_agent import UserInteractionAgent
from agents.memory_agent import MemoryAgent
from agents.itinerary_agent import ItineraryAgent
from agents.weather_agent import WeatherAgent
from agents.optimization_agent import OptimizationAgent
from agents.gemini_agent import GeminiAgent
from agents.news_agent import NewsAgent
import geocoder

# Path to your CSS file
css_file_path = os.path.join(os.path.dirname(__file__), "style.css")


# Function to load and apply CSS
def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Initialize agents
memory_agent = MemoryAgent()
user_interaction_agent = UserInteractionAgent(memory_agent)
itinerary_agent = ItineraryAgent(memory_agent)
weather_agent = WeatherAgent()
gemini_agent = GeminiAgent()
optimization_agent = OptimizationAgent(memory_agent)
map_agent = MapAgent()
news_agent = NewsAgent()

# Apply the CSS
load_css(css_file_path)


def get_weather(city, date):
    try:
        return weather_agent.get_weather(city, date)
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None


def generate_suggestions(city):
    prompt = f"Provide a list of up to 5 activities in {city} for travelers interested in food, adventure, culture, and local experiences. Each activity should be a short, catchy name."

    try:
        generated_text = gemini_agent.query(prompt)
        if generated_text:
            suggestions = [
                line.strip() for line in generated_text.split("\n") if line.strip()
            ]
            return suggestions[:5] if len(suggestions) <= 5 else suggestions
        else:
            return ["Sorry, I couldn't generate suggestions at this time."]
    except Exception as e:
        st.error(f"Error fetching suggestions: {e}")
        return ["Sorry, there was an error while generating suggestions."]


def plan_trip(
    city, start_time, end_time, budget, interests, date_input, starting_point
):
    if start_time >= end_time:
        st.error("Start time should be earlier than end time.")
        return

    user_preferences = {
        "city": city,
        "start_time": start_time,
        "end_time": end_time,
        "interests": [interest.strip() for interest in interests.split(",")],
        "budget": budget,
        "date_input": date_input,
        "starting_point": starting_point,
    }

    user_interaction_agent.gather_user_preferences(user_preferences)

    # Store each preference in memory
    for key, value in user_preferences.items():
        memory_agent.store_preference(key, value)

    # Fetch weather
    weather_data = get_weather(city, date_input.strftime("%Y-%m-%d"))
    if weather_data:
        description = weather_data.get("description", "No description available")
        temperature = weather_data.get("temperature", "N/A")
        st.subheader(f"Weather: {city} has {description} with {temperature}° C.")

    # Generate itinerary
    itinerary = itinerary_agent.generate_itinerary(
        city, interests, date_input, starting_point
    )
    if not itinerary:
        st.error("Itinerary generation failed. Please try again.")
        return

    # Optimize itinerary
    current_date = datetime.today().date()  # Get today's date
    start_time = datetime.combine(
        current_date, start_time
    )  # Combines current date with start time
    end_time = datetime.combine(
        current_date, end_time
    )  # Combines current date with end time

    optimized_itinerary = optimization_agent.optimize_path(
        itinerary, budget, start_time, end_time
    )
    if optimized_itinerary:
        st.write(optimized_itinerary)
    else:
        st.error(
            "Optimization failed. The itinerary might not fit within time constraints."
        )

    # News related to the trip
    news = news_agent.fetch_and_check_news(optimized_itinerary, city)
    st.header("News that might affect our plan:")
    st.write(news)

    # Map generation
    locations = optimization_agent.locations_from_itinerary(optimized_itinerary)
    map_url = map_agent.create_map_url(locations)
    st.header("Tour Map")
    st.write(map_url)
    st.components.v1.html(
        f"<iframe width='100%' height='500' frameborder='0' style='border:0' src='{map_url}' allowfullscreen></iframe>",
        height=500,
    )


def main():
    st.markdown(
        """
        <div class="title-container">
            <div class="title">Tour Planning Assistant</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Initialize session state variables for user inputs
    if "city" not in st.session_state:
        st.session_state.city = ""
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.now().time()
    if "end_time" not in st.session_state:
        st.session_state.end_time = datetime.now().time()
    if "budget" not in st.session_state:
        st.session_state.budget = 2000
    if "interests" not in st.session_state:
        st.session_state.interests = ""
    if "starting_point" not in st.session_state:
        st.session_state.starting_point = ""
    if "date_input" not in st.session_state:
        st.session_state.date_input = datetime.today().date()

    st.session_state.city = st.text_input(
        "Enter your destination city:", st.session_state.city
    )
    st.session_state.start_time = st.time_input(
        "Start time of your tour:", st.session_state.start_time
    )
    st.session_state.end_time = st.time_input(
        "End time of your tour:", st.session_state.end_time
    )
    st.session_state.budget = st.number_input(
        "Enter your budget (INR):", value=st.session_state.budget, step=500
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        interests_input = st.text_input(
            "Enter your interests (comma-separated)",
            value=st.session_state.interests,
            key="interests",
        )
        if interests_input != st.session_state.interests:
            st.session_state.interests = interests_input

    with col2:
        if st.button("Wanna know interesting things in city?"):
            if st.session_state.city:
                suggestions = generate_suggestions(st.session_state.city)
                st.session_state.suggestions = suggestions
            else:
                st.write("Please enter your city first to get suggestions.")

    if "suggestions" in st.session_state:
        st.divider()
        st.write("**Here are some suggestions for things to do in the city:**")
        for suggestion in st.session_state.suggestions:
            st.write(f"- {suggestion}")

        with st.expander("More options:", expanded=False):
            st.divider()

            # Fetch current location using geocoder
            def fetch_location():
                g = geocoder.ip("me")
                if g.ok:
                    return g.address  # Return address if geocoder is successful
                else:
                    return "Unknown location"  # Fallback if location cannot be fetched

            location = fetch_location()  # Call function to get location
            st.session_state.starting_point = st.text_input(
                "Starting point of your journey:",
                value=st.session_state.starting_point
                or location,  # Use fetched location if available
            )
            st.session_state.date_input = st.date_input(
                "Select the date of your tour", value=st.session_state.date_input
            )

    if st.button("Plan My Trip"):
        plan_trip(
            st.session_state.city,
            st.session_state.start_time,
            st.session_state.end_time,
            st.session_state.budget,
            st.session_state.interests,
            st.session_state.date_input,
            st.session_state.starting_point,
        )


if __name__ == "__main__":
    main()
