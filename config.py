import os
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
CELERY_BROKER_URL = BROKER_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')