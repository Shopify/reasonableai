import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Ability:
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return f"Ability(name='{self.name}', description='{self.description}')"

class SemanticNetwork:
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return f"SemanticNetwork(name='{self.name}', description='{self.description}')"

class Competencies:
    def __init__(self):
        self.abilities = []
        self.semantic_networks = []
        self._load_abilities()
        self._load_semantic_networks()

    @property
    def all(self):
        return self.abilities + self.semantic_networks

    def _load_abilities(self):
        ability_urls = os.getenv("ABILITY_URLS")

        if ability_urls:
            for ability_url in ability_urls.split(","):
                response = requests.get(f"{ability_url}/documentation").json()
                self.abilities.append(Ability(response['name'], response['description'], ability_url))

    def _load_semantic_networks(self):
        semantic_network_urls = os.getenv("SEMANTIC_NETWORK_URLS")

        if semantic_network_urls:
            for semantic_network_url in semantic_network_urls.split(","):
                response = requests.get(f"{semantic_network_url}/documentation").json()
                self.semantic_networks.append(SemanticNetwork(response['name'], response['description'], semantic_network_url))

    def __repr__(self):
        return f"Competencies({len(self.abilities)} abilities and {len(self.semantic_networks)} semantic_networks)"
