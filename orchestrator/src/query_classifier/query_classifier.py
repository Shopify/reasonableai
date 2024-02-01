from jinja2 import Environment, FileSystemLoader
from ..models.ability import Ability
from ..models.semantic_network import SemanticNetwork
from ..utils.query_llm import QueryLLM

class QueryClassifier:
    def __init__(self, user_query):
        self.user_query = user_query
        self.compentencies = [
            Ability("GitHub", "Read GitHub repos, create pull requests and issues", "http://github.com"),
            Ability("Researcher", "Search the web information, returns appropriate documents. Useful for finding facts", "http://google.com"),
            SemanticNetwork("Tigers", "Information about Tigers, their habits, ranges, diets, etc", "http://tigers.com"),
            SemanticNetwork("Lions", "Information about Lions, their habits, ranges, diets, etc", "http://lions.com"),
            SemanticNetwork("Cats", "Information about house cats, their habits, naps, diets, etc", "http://cats.com")
        ] #this will be replaced with a global variable or model

    def classify(self):
        prompt_env = Environment(loader=FileSystemLoader('prompts'))
        template = prompt_env.get_template('query_classifier.j2')
        reasoning_prompt = template.render(prompt=self.user_query, compentencies=self.compentencies)
        return QueryLLM(reasoning_prompt).response['message']['content']
