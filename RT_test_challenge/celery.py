import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RT_test_challenge.settings')

app = Celery('RT_test_challenge')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
