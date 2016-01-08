from flask import Flask
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Flask(__name__)
celery = Celery(app.name, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.config.from_object('config')
from app import views