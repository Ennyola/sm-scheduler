import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
if os.environ.get("DEBUG", False):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.production")

app = Celery("sm_scheduler")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
