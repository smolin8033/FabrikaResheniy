import json
import datetime

import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.shortcuts import get_object_or_404

from message.models import Message
from message.services.send_messages_service import send_message

logger = get_task_logger(__name__)


TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI6ImZhYnJ"
    "pcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo"
)
HEADERS = {"Authorization": "Bearer {}".format(TOKEN)}


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    for msg_id in messages_ids:
        send_message(msg_id)


@shared_task
def send_not_sent_message(message_id):
    messages = Message.objects.filter(
        status=False, mailing__end_datetime__lte=datetime.datetime.now()
    )
    print(messages)
