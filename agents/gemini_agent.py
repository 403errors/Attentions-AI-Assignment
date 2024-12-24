import toml
import google.generativeai as genai

secrets = toml.load("secrets.toml")

# Google API Key for Bard
API_KEY = secrets["GEMINI_API_KEY"]

# Configure generative AI with API key
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = genai.types.GenerationConfig(
    temperature=0.9,
    top_p=1,
    top_k=1,
    max_output_tokens=8192,
)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

class GeminiAgent:
    def __init__(self):
        """
        Initialize the GeminiAgent with the API key.
        """
        self.api_key = API_KEY

    def query(self, prompt):
        """
        Query the Gemini (Bard) model with a prompt and return the response.
        """
        try:
            # Generate content with the model using the prompt
            response = model.generate_content(prompt)

            # Return the response text from the model
            return response.text

        except Exception as e:
            print(f"An error occurred while querying Gemini API: {e}")
            return None  # Optionally return None or some error message
