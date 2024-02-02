from celery import Celery
from dotenv import load_dotenv
import os
# from .src.utils.competencies import Competencies

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
# COMPENTENCIES = Competencies()

app = Celery('tasks', broker=RABBITMQ_HOST)
