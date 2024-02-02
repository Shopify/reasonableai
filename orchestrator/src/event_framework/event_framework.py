import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

app = Celery('tasks', broker=RABBITMQ_HOST)
@app.task
def add(x, y):
    return x + y