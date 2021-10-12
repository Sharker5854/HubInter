import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hubinter.settings')

app = Celery('hubinter')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

'''
Command to start worker process (on Windows need "-P gevent"):

celery -A hubinter worker -l info -P gevent
'''