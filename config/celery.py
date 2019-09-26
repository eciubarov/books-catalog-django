import os
from decouple import config
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('demobooks')
app.config_from_object('django.conf:settings')
app.conf.update(BROKER_URL=config('REDIS_URL'),
                CELERY_RESULT_BACKEND=config('REDIS_URL'))
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()