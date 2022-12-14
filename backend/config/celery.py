import os

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "message.tasks.send_not_sent_message",
        "schedule": crontab("*/2"),
    },
}

app.conf.task_routes = {
    "message.tasks.send_not_sent_message": {"queue": "queue_for_single_worker"}
}


app.conf.timezone = "Europe/Moscow"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
