# from neo4j import GraphDatabase
# from neo4j import GraphDatabase
import toml
secrets = toml.load("secrets.toml")

# load_dotenv()

# class Neo4jAgent:
#     def __init__(self):
#         uri = secrets["NEO4J_URI"]
#         user = secrets["NEO4J_USER"]
#         password = secrets["NEO4J_PASSWORD"]
#         self.driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self.driver.close()

#     def add_preference(self, user_id, key, value):
#         query = (
#             "MERGE (u:User {id: $user_id}) "
#             "MERGE (p:Preference {key: $key, value: $value}) "
#             "MERGE (u)-[:PREFERS]->(p)"
#         )
#         with self.driver.session() as session:
#             session.run(query, user_id=user_id, key=key, value=value)

#     def get_preferences(self, user_id):
#         query = (
#             "MATCH (u:User {id: $user_id})-[:PREFERS]->(p:Preference) "
#             "RETURN p.key AS key, p.value AS value"
#         )
#         with self.driver.session() as session:
#             results = session.run(query, user_id=user_id)
#             return {record["key"]: record["value"] for record in results}


# # example
# neo_agent = Neo4jAgent()

# # Add a user preference
# neo_agent.add_preference("user123", "interest", "historical sites")

# # Fetch preferences
# preferences = neo_agent.get_preferences("user123")
# print(preferences)  # {'interest': 'historical sites'}


# agents/memory_agent.py


class MemoryAgent:
    def __init__(self):
        self.user_memory = {}  # Dictionary to store user preferences over time

    def store_preference(self, key, value):
        """Store a preference with a key and value."""
        # Store preferences as they come in, allowing historical tracking
        self.user_memory[key] = value

    def get_preference(self, key):
        """Retrieve a preference by its key."""
        return self.user_memory.get(key, None)
