import json

class JsonExtractor:
    def __init__(self, disorganized_string):
        self.disorganized_string = disorganized_string

    def extract(self):
        start_index = self.disorganized_string.find('{')
        end_index = self.disorganized_string.rfind('}')

        if start_index == -1 or end_index == -1:
            raise ValueError("No JSON blob found in the string")

        json_str = self.disorganized_string[start_index:end_index+1]
        json_obj = json.loads(json_str)
        return json_obj
