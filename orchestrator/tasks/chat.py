import requests
from celery_app import app, ORCHESTRATOR_WEB_URL
from src.query_classifier.query_classifier import QueryClassifier
from src.utils.load_settings import SEMANTIC_NETWORKS, ABILITIES, DESIRES

def process_incoming_message(message):
    print('Processing incoming message: {}'.format(message))
    print('Classifying message...')
    query_classification = QueryClassifier(message).classify()
    print(f'Classification results: {query_classification}')
    message = f"These are the results of the query classification: {query_classification}"
    print(f"Posting message to chat: {message}")
    app.send_task('post_message_to_chat', kwargs={'message': message})

def post_message_to_chat(message):
    # there is a much better way to do this but it's getting late on Hack Days
    print(f"Recieved message to post to chat: {message}")
    url = f"{ORCHESTRATOR_WEB_URL}/receive_bot_message"
    data = {'message': message}
    print(f"Posting message to {url}")
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Message posted successfully to {url}")
    else:
        print(f"Failed to post message to {url}.\nStatus code: {response.status_code}\nMessage: {message}.")
