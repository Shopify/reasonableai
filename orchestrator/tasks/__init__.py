from celery_app import app
from .maintenance import startup
from .chat import process_incoming_message, post_message_to_chat

app.task(name='maintenance.startup')(startup)
app.task(name='process_incoming_message')(process_incoming_message)
app.task(name='post_message_to_chat')(post_message_to_chat)
