import requests
import json
import random
from celery_app import app, ORCHESTRATOR_WEB_URL
from jinja2 import Environment, FileSystemLoader
from src.utils.query_llm import QueryLLM
from src.utils.load_settings import SEMANTIC_NETWORKS
from src.utils.text_extractor import extract_first_sentence

prompt_env = Environment(loader=FileSystemLoader('prompts/jokes'))
jokes_symantic_network_url = next(sn.url for sn in SEMANTIC_NETWORKS if sn.name == 'Jokes')
headers = {"Content-Type": "application/json"}

def generate_joke_setup():
    print('Generating joke setup...')
    template = prompt_env.get_template('generate_joke_setup.j2')
    generate_joke_setup_prompt = template.render()
    joke_setup_response = QueryLLM(
        generate_joke_setup_prompt,
        model='mixtral:latest',
        temperature=1
    ).response['message']['content']
    print(f'Generated joke setup: {joke_setup_response}')

    joke_setup = extract_first_sentence(joke_setup_response)
    print(f'Using joke setup: {joke_setup}')

    data = json.dumps({
        "document": joke_setup,
        "keywords": ["setup"],
        "trustworthiness": 0.6
    })

    print(f"Posting joke setup to semantic network: {jokes_symantic_network_url}")
    response = requests.post(
        f"{jokes_symantic_network_url}/nodes",
        headers=headers,
        data=data
    )

    if response.status_code == 201:
        print(f"Posted joke setup to semantic network: {response.status_code}")
    else:
        print(f"Failed to post joke setup to semantic network: {response.json()}")

def generate_joke_punchline():
    print('Generating joke punchline...')
    template = prompt_env.get_template('generate_joke_punchline.j2')
    generate_joke_punchline_prompt = template.render()
    joke_punchline_response = QueryLLM(
        generate_joke_punchline_prompt,
        model='mixtral:latest',
        temperature=1
    ).response['message']['content']
    print(f'Generated joke punchline: {joke_punchline_response}')

    joke_punchline = extract_first_sentence(joke_punchline_response)
    print(f'Using joke punchline: {joke_punchline}')

    data = json.dumps({
        "document": joke_punchline,
        "keywords": ["punchline"],
        "trustworthiness": 0.6
    })

    print(f"Posting joke punchline to semantic network: {jokes_symantic_network_url}")
    response = requests.post(
        f"{jokes_symantic_network_url}/nodes",
        headers=headers,
        data=data
    )

    if response.status_code == 201:
        print(f"Posted joke punchline to semantic network: {response.status_code}")
    else:
        print(f"Failed to post joke punchline to semantic network: {response.json()}")

def create_joke():
    print('Creating joke...')

    print('Collecting setup...')
    setup_serach = requests.get(f"{jokes_symantic_network_url}/search", params={"keywords": "setup"})
    setup = random.choice(setup_serach.json())

    print('Collecting punchline...')
    punchline_search = requests.get(f"{jokes_symantic_network_url}/search", params={"keywords": "punchline", "min_trustworthiness": 0.6})
    punchline = random.choice(punchline_search.json())

    joke = f"{setup['document']}\n{punchline['document']}"
    print(f'Using joke: {joke}')

    template = prompt_env.get_template('rate_joke.j2')
    generate_rate_joke_prompt = template.render(joke=joke)
    rate_joke_response = QueryLLM(
        generate_rate_joke_prompt,
        model='deepseek-llm:67b-chat',
        temperature=0,
        json_response=True
    ).response['message']['content']
    print(f'Generated joke rating: {rate_joke_response}')

    rating = (
        min(rate_joke_response["SO"], 0.7) *
        min(rate_joke_response["LM"], 0.6) *
        min(rate_joke_response["PU"], 0.9) *
        min(rate_joke_response["SE"], 0.9) *
        min(rate_joke_response["GR"], 0.9)
    )

    print(f"Rating of {rating} for this joke:\n{joke}")

    data = json.dumps({
        "target_id": punchline['node_id'],
        "weight": rating,
    })

    print(f"Posting joke relationship to semantic network: {jokes_symantic_network_url}")
    response = requests.post(
        f"{jokes_symantic_network_url}/nodes/{setup['node_id']}/relationships",
        headers=headers,
        data=data
    )

    if response.status_code == 201:
        print(f"Posted joke relationship to semantic network: {response.status_code}")
    else:
        print(f"Failed to post relationship setup to semantic network: {response.json()}")
