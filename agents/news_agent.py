import requests
import os

API_KEY = os.getenv("NEWS_API")


class NewsAgent:
    """
    NewsAgent class fetches news related to the itinerary and destination
    to inform users of potential events or issues affecting their plans.
    """

    def __init__(self):
        """
        Initializes the NewsAgent with the required API key.

        Args:
            api_key (str): API key for News API.
        """
        self.api_key = API_KEY
        self.news_api_url = "https://newsapi.org/v2/everything"
        # Keywords that might indicate a disruption to the plans
        self.impact_keywords = [
            "cancellation",
            "delayed",
            "closed",
            "strike",
            "disruption",
            "postponed",
            "weather",
            "accident",
            "traffic",
            "storm",
            "roadblock",
        ]

    def fetch_news(self, itinerary: list, destination: str) -> list:
        """
        Fetches news articles related to the itinerary and destination.

        Args:
            itinerary (list): List of planned activities or locations.
            destination (str): The place of visit or city name.

        Returns:
            list: A list of relevant news articles as dictionaries (title and description).
        """
        # Create a search query based on the itinerary and destination
        query = f"{destination} news OR events OR disruptions OR activities"

        params = {
            "q": query,
            "apiKey": self.api_key,
            "pageSize": 5,  # Limit number of results
            "language": "en",  # Filter results to English articles
        }

        response = requests.get(self.news_api_url, params=params)

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            # Extract relevant information
            news_list = [
                {"title": article["title"], "description": article["description"]}
                for article in articles
            ]
            return news_list
        else:
            print(f"Error: Unable to fetch news. Status code: {response.status_code}")
            return []

    def check_impact(self, news_list: list) -> list:
        """
        Checks whether the fetched news articles contain keywords
        that might affect the travel plans.

        Args:
            news_list (list): List of news articles as dictionaries.

        Returns:
            list: List of articles that might affect the plans.
        """
        impacted_articles = []

        for news in news_list:
            title, description = news["title"], news["description"]
            # Check if any of the impact keywords are present in the title or description
            if any(
                keyword.lower() in (title + description).lower()
                for keyword in self.impact_keywords
            ):
                impacted_articles.append(news)

        return impacted_articles

    def generate_bullet_points(self, impacted_articles: list) -> str:
        """
        Converts the list of impacted news articles into bullet point strings.

        Args:
            impacted_articles (list): List of impacted news articles as dictionaries.

        Returns:
            str: News in bullet-point format.
        """
        if not impacted_articles:
            return "No relevant news found that might affect your plans."

        bullet_points = "\n".join(
            [
                f"- **{news['title']}**: {news['description']}"
                for news in impacted_articles
            ]
        )
        return bullet_points

    def fetch_and_check_news(self, itinerary: list, destination: str) -> str:
        """
        Fetches and checks news articles to see if any disruptions might affect the plans.

        Args:
            itinerary (list): List of planned activities or locations.
            destination (str): The place of visit or city name.

        Returns:
            str: Bullet-point list of news that could affect the plan.
        """
        news_list = self.fetch_news(itinerary, destination)
        impacted_articles = self.check_impact(news_list)
        return self.generate_bullet_points(impacted_articles)
