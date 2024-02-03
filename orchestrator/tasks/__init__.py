from celery_app import app
from .maintenance import startup
from .chat import process_incoming_message, post_message_to_chat
from .jokes import generate_joke_setup, generate_joke_punchline, create_joke

app.task(name='maintenance.startup')(startup)
app.task(name='process_incoming_message')(process_incoming_message)
app.task(name='post_message_to_chat')(post_message_to_chat)
app.task(name='generate_joke_setup')(generate_joke_setup)
app.task(name='generate_joke_punchline')(generate_joke_punchline)
app.task(name='create_joke')(create_joke)
