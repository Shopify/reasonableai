import yaml
from src.models.ability import Ability
from src.models.semantic_network import SemanticNetwork
from src.models.desire import Desire

with open('settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

print(f"Loaded settings: {settings}")

SEMANTIC_NETWORKS = []
if settings.get('semantic_networks'):
    for semantic_network_settings in settings['semantic_networks']:
        semantic_network = SemanticNetwork(
            semantic_network_settings['name'],
            semantic_network_settings['description'],
            semantic_network_settings['url']
        )
        SEMANTIC_NETWORKS.append(semantic_network)

print(f'Loaded semantic networks: {SEMANTIC_NETWORKS}')

ABILITIES = []
if settings.get('abilities'):
    for ability_settings in settings['abilities']:
        ability = Ability(
            ability_settings['name'],
            ability_settings['description'],
            ability_settings['url']
        )
        ABILITIES.append(ability)

print(f'Loaded abilities: {ABILITIES}')

DESIRES = []
if settings.get('desires'):
    for desire_settings in settings['desires']:
        desire = Desire(
            desire_settings['name'],
            desire_settings['description'],
            desire_settings['priority']
        )
        DESIRES.append(desire)

print(f'Loaded desires: {DESIRES}')
