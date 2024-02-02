from jinja2 import Environment, FileSystemLoader
from ..utils.query_llm import QueryLLM
from ..utils.load_settings import SEMANTIC_NETWORKS, ABILITIES

class QueryClassifier:
    def __init__(self, user_query):
        self.user_query = user_query
        self.compentencies = SEMANTIC_NETWORKS + ABILITIES

    def classify(self):
        prompt_env = Environment(loader=FileSystemLoader('prompts'))
        template = prompt_env.get_template('query_classifier.j2')
        reasoning_prompt = template.render(prompt=self.user_query, compentencies=self.compentencies)
        query_classification = QueryLLM(reasoning_prompt, json_response=True).response['message']['content']
        sorted_query_classification = sorted(query_classification['ratios'], key=lambda x: x['relevance'], reverse=True)
        return sorted_query_classification
