import os
import json
import requests
import time
from dotenv import load_dotenv
from ..utils.json_extractor import JsonExtractor
from ..utils.load_settings import OLLAMA_URL

load_dotenv()

class QueryLLM:
    def __init__(self, prompt, model='mixtral:latest', temperature=0.0, json_response=False):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.json_response = json_response
        self.response = self.get_response()

    def _json_request(self):
        return json.dumps(
            {
                "model": "mixtral:latest",
                "stream": False,
                "messages": [ { "role": "user", "content": self.prompt } ],
                "options": {
                    "temperature": self.temperature
                }
            }
        )

    def _send_request(self):
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = self._json_request()
        ollama_api_url = f"{OLLAMA_URL}/api/chat"
        response = requests.post(ollama_api_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {OLLAMA_URL} responded with status code {response.status_code}")

    def get_response(self, tries=2):
        backoff_time = 1
        for i in range(tries):
            try:
                response = self._send_request()
                if self.json_response:
                    response["message"]["content"] = JsonExtractor(response["message"]["content"]).extract()
            except Exception as e:
                print(e)
                backoff_time *= 2
                print(f"Waiting {backoff_time} seconds...")
                time.sleep(backoff_time)
                print(f"Retrying {i+1} of {tries}")
        return response