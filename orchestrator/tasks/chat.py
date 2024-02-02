import time
import requests
from .celery_app import app

def process_incoming_message(message):
    print('Processing incoming message: {}'.format(message))
    time.sleep(2)
    # Enqueue the post_message_to_chat task
    app.send_task('post_message_to_chat', kwargs={'message': 'hello world'})

def post_message_to_chat(message):
    # there is a much better way to do this but it's getting late on Hack Days
    url = "http://127.0.0.1:5000/receive_bot_message"
    data = {'message': message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Message posted successfully: {message}")
    else:
        print(f"Failed to post message: {message}. Status code: {response.status_code}")
