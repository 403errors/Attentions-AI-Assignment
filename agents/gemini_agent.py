import os
import google.generativeai as genai

# Google API Key for Bard
API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiAgent:
    def __init__(self):
        """
        Initialize the GeminiAgent with the API key.
        """
        self.api_key = API_KEY
        genai.configure(api_key=self.api_key)

    def query(self, prompt):
        """
        Query the Gemini (Bard) model with a prompt and return the response.
        """
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content with the model using the prompt
            response = model.generate_content(prompt)

            # Return the response text from the model
            return response.text

        except Exception as e:
            print(f"An error occurred while querying Gemini API: {e}")
            return None  # Optionally return None or some error message
