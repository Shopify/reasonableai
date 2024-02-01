import os
import requests
import json
import pytest
from jinja2 import Environment, FileSystemLoader
from ..src.utils.compentencies import Ability, SemanticNetwork
from ..src.utils.json_extractor import JsonExtractor

env = Environment(loader=FileSystemLoader('../prompts'))
host = os.getenv("OLLAMA_URL")
compentencies = [
    Ability("GitHub", "Read GitHub repos, create pull requests and issues", "http://github.com"),
    Ability("Researcher", "Search the web information, returns appropriate documents. Useful for finding facts", "http://google.com"),
    SemanticNetwork("Tigers", "Information about Tigers, their habits, ranges, diets, etc", "http://tigers.com"),
    SemanticNetwork("Lions", "Information about Lions, their habits, ranges, diets, etc", "http://lions.com"),
    SemanticNetwork("Cats", "Information about house cats, their habits, naps, diets, etc", "http://cats.com")
]

def request_data(prompt, model='mixtral:latest'):
    return json.dumps(
        {
            "model": model,
            "stream": False,
            "messages": [ { "role": "user", "content": prompt } ]
        }
    )

def llm_response(template_file, prompt):
    template = env.get_template(template_file)
    reasoning_prompt = template.render(prompt=prompt, compentencies=compentencies)
    response = requests.post(f"{host}/api/chat", data=request_data(reasoning_prompt))

    llm_response = response.json()["message"]["content"]
    return JsonExtractor(llm_response).extract()


def test_query_classifier_with_cat_question():
    actual = llm_response('query_classifier.j2', "Where do big wild cats live?")

    assert len(actual['ratios']) == len(compentencies)

    expected_ranges = {
        'GitHub': (0, 0.1),
        'Researcher': (0.4, 0.7),
        'Tigers': (0.5, 1.0),
        'Lions': (0.5, 1.0),
        'Cats': (0.1, 0.4)
    }

    for ratio in actual['ratios']:
        topic_name = ratio['topic name']
        if topic_name in expected_ranges:
            lower, upper = expected_ranges[topic_name]
            assert lower <= ratio['relevance'] <= upper

def test_query_classifier_with_github_question():
    actual = llm_response('query_classifier.j2', "When was the last commit to the ReasonAbleAI repo?")

    assert len(actual['ratios']) == len(compentencies)

    expected_ranges = {
        'GitHub': (0.7, 1.0),
        'Researcher': (0.1, 0.5),
        'Tigers': (0.0, 0.1),
        'Lions': (0.0, 0.1),
        'Cats': (0.0, 0.1)
    }

    for ratio in actual['ratios']:
        topic_name = ratio['topic name']
        if topic_name in expected_ranges:
            lower, upper = expected_ranges[topic_name]
            assert lower <= ratio['relevance'] <= upper
