class UserInteractionAgent:
    def __init__(self, memory_agent):
        self.memory_agent = memory_agent  # MemoryAgent to track previous preferences
        self.user_preferences = {}  # Store the current session's preferences

    def gather_user_preferences(self, new_preferences):
        """Gather preferences like city, timings, and interests from the user."""

        # Update the current session's user preferences
        self.user_preferences = new_preferences

        # Store the new preferences in memory to keep historical data
        for key, value in new_preferences.items():
            self.memory_agent.store_preference(key, value)

        return self.user_preferences


if __name__ == "__main__":

    user_preferences = {
        "city": "Delhi",
        "interests": ["history", "food"],
        "budget": 2000,
        "start_time": "9:00 AM",
        "end_time": "6:00 PM",
        "starting_point": "Hotel Roma",
    }
