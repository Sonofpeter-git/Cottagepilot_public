import os
from celery import Celery
from django.utils.timezone import now
from tasks.models import Task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorhub.settings')

app = Celery('sensorhub')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# aLoad task modules from all registered Django pps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def mark_overdue():
    overdue_time = Task.objects.filter(time_correlation=now(), status__ne='overdue')
    overdue_time.update(status='overdue')

    #Add overdue function to trigger values from sensors