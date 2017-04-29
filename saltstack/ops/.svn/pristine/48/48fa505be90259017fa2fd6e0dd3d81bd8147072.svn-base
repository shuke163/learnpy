from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sm.settings')

app = Celery('sm')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'host-sync-every-1800-seconds': {
        'task': 'job.tasks.hostSyncTask',
        'schedule': 1800.0,
    },
    'service-job-every-60-seconds': {
        'task': 'service.tasks.syncJobStatus',
        'schedule': 60.0,
    },
}
