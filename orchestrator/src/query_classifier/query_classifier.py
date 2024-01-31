import os
import json
import requests
from dotenv import load_dotenv
from ..utils.classifier_prompt import CLASSIFIER_PROMPT
from ..utils.json_extractor import JsonExtractor

load_dotenv()

class QueryClassifier:
    def __init__(self, user_query):
        self.user_query = user_query
    
    def classify(self):
        host = os.getenv("ORCHESTRATOR_SERVER", "localhost")
        username = os.getenv("ORCHESTRATOR_USERNAME", "")
        password = os.getenv("ORCHESTRATOR_PASSWORD", "")
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        response = requests.post(host, headers=headers, data=self.json_request(), auth=(username, password))
        if response.status_code == 200:
            llm_response = response.json()["message"]["content"]
            return JsonExtractor(llm_response).extract()
        else:
            print(f"Error with request, status code: {response.status_code}")
            raise Exception("Error with request")

    def json_request(self):
        return json.dumps(
            {
                "model": "mixtral:latest",
                "stream": False,
                "messages": [ { "role": "user", "content": self.formulate_request() } ]
            }
        )
    
    def formulate_request(self):
        return CLASSIFIER_PROMPT.format(query = self.user_query)

QueryClassifier("What is the weather like today?").classify()