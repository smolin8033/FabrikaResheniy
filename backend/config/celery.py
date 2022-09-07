import os

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.task_routes = {"message.tasks.send_not_sent_message": {"queue": "periodic"}}
app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "message.tasks.send_not_sent_message",
        "schedule": crontab(minute="*/2"),
    },
}

app.conf.timezone = "Europe/Moscow"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
