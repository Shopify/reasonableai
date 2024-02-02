import time
import requests
from celery_app import app
from src.query_classifier.query_classifier import QueryClassifier
from src.utils.load_settings import SEMANTIC_NETWORKS, ABILITIES, DESIRES

def process_incoming_message(message):
    print('Processing incoming message: {}'.format(message))
    print('Classifying message...')
    print(f"Semantic networks: {SEMANTIC_NETWORKS}")
    print(f"Abilities: {ABILITIES}")
    print(f"Desires: {DESIRES}")
    query_classification = QueryClassifier(message).classify()
    print(f'Classification results: {query_classification}')
    most_relevant_topic = query_classification[0]
    message = f"The most relevant topic is: {most_relevant_topic['topic name']}"
    print(f"Posting message to chat: {message}")
    app.send_task('post_message_to_chat', kwargs={'message': message})

def post_message_to_chat(message):
    # there is a much better way to do this but it's getting late on Hack Days
    print(f"Recieved message to post to chat: {message}")
    url = "http://127.0.0.1:5000/receive_bot_message"
    data = {'message': message}
    print(f"Posting message to chat: {message}")
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Message posted successfully: {message}")
    else:
        print(f"Failed to post message: {message}. Status code: {response.status_code}")
