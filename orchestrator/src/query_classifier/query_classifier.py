from jinja2 import Environment, FileSystemLoader
from ..utils.query_llm import QueryLLM
from ..utils.load_settings import SEMANTIC_NETWORKS, ABILITIES, DESIRES

class QueryClassifier:
    def __init__(self, user_query):
        self.user_query = user_query

    META_QUESTIONS =[
            'the prompt is a single question',
            'the prompt has multiple questions',
            'the prompt is a single command',
            'the prompt has multiple commands',
            'the prompt is a single statement',
            'the prompt has multiple statements',
            'the prompt requires a response',
            'the prompt involves multiple semantic networks',
            'the prompt involves multiple abilities',
            'the prompt involves multiple desires',
            'the prompt is urgent',
        ]

    def _get_highest_ranked_elements(self, query_classification):
        combined_list = query_classification['semantic networks'] + query_classification['abilities']
        sorted_combined_list = sorted(combined_list, key=lambda x: x['relevance'], reverse=True)
        highest_relevance = sorted_combined_list[0]['relevance']
        highest_ranked_elements = [element for element in sorted_combined_list if element['relevance'] == highest_relevance]
        return highest_ranked_elements

    def _get_highest_ranked_meta_questions(self, query_classification):
        sorted_meta_questions = sorted(query_classification['meta questions'], key=lambda x: x['accuracy'], reverse=True)
        highest_accuracy = sorted_meta_questions[0]['accuracy']
        highest_ranked_meta_questions = [question for question in sorted_meta_questions if question['accuracy'] == highest_accuracy]
        return highest_ranked_meta_questions

    def classify(self):
        prompt_env = Environment(loader=FileSystemLoader('prompts'))
        template = prompt_env.get_template('query_classifier.j2')
        reasoning_prompt = template.render(
            prompt=self.user_query,
            semantic_networks=SEMANTIC_NETWORKS,
            abilities=ABILITIES,
            desires=DESIRES,
            meta_questions=self.META_QUESTIONS
        )
        query_classification = QueryLLM(reasoning_prompt, json_response=True).response['message']['content']
        highest_ranked_elements = self._get_highest_ranked_elements(query_classification)
        highest_ranked_meta_questions = self._get_highest_ranked_meta_questions(query_classification)
        return {
            'highest_ranked_elements': highest_ranked_elements,
            'highest_ranked_meta_questions': highest_ranked_meta_questions,
            'query_classification': query_classification
        }
