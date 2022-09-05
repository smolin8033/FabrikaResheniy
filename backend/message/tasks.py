import json

import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.shortcuts import get_object_or_404

from message.models import Message

logger = get_task_logger(__name__)


TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI6ImZhYnJ' \
            'pcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo'
HEADERS = {
    'Authorization': 'Bearer {}'.format(TOKEN)
}


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    for message_id in messages_ids:
        data = {
            'id': message_id,
            'phone': 0,
            'text': 'string'
        }
        service_url = f'https://probe.fbrq.cloud/v1/send/{message_id}'
        response = requests.post(service_url, headers=HEADERS, data=json.dumps(data))
        if not response.ok:
            message = get_object_or_404(Message, id=message_id)
            with transaction.atomic():
                message.status = True
                message.save()
        else:
            send_not_sent_message(message_id)


@shared_task
def send_not_sent_message(message_id):
    data = {
        'id': message_id,
        'phone': 0,
        'text': 'string'
    }
    service_url = f'https://probe.fbrq.cloud/v1/send/{message_id}'
    response = requests.post(service_url, headers=HEADERS, data=json.dumps(data))
    if response.ok:
        message = get_object_or_404(Message, id=message_id)
        with transaction.atomic():
            message.status = True
            message.save()
