from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

app = Celery('tasks', broker=RABBITMQ_HOST)
app.conf.update(
    CELERY_IMPORTS=("tasks",)
)
