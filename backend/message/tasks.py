import requests

from celery import shared_task
from celery.utils.log import get_task_logger

from config.celery import app


logger = get_task_logger(__name__)


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    pass
    # for message_id in messages_ids:
    #     response = requests.post()
