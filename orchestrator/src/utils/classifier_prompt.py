CLASSIFIER_PROMPT = """"
Read through all the instructions before beginning and follow them in order. Do not deviate from the instructions or make things up.

Instructions:

Given the following prompt, your task is to create a JSON Blob object with the structure: {{ "ratios": [{{"confidence": <confidence_score>, "topic": <relevant_topic>}}] }} where:
<confidence_score> is a confidence score between 0 and 1 representing how confident you are that the prompt relates to the given topics, always include every topic in the result.
<relevant_topic> is a string indicating which topic from the list [Python Coding,  Ruby Coding, Tigers] the prompt is most relevant to (exactly as written, with the brackets and all). If the prompt is not related to any of the given topics, use "None" as the value for <relevant_topic>.
Example response: {{ "ratios": [{{"confidence": 0.95, "topic": "Python Coding"}}, {{"confidence": 0.3, "topic": "Ruby Coding"}}, {{"confidence": 0.7, "topic": "Tigers"}}]}}
Return ONLY the JSON Blob object, nothing else.

Prompt: "{query}"
"""