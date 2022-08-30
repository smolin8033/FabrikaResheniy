import json
import os

import requests

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def send_messages(messages_ids=None):
    """
    Отправка сообщений
    """
    if messages_ids is None:
        messages_ids = []

    headers = {"Authorization": os.token()}

    for message_id in messages_ids:
        data = {
            "id": message_id,
            "phone": 0,
            "text": "string"
        }
        service_url = f"https://probe.fbrq.cloud/v1/send/{message_id}"
        response = requests.post(service_url, headers=headers, data=json.dumps(data))
        response.ok

# response = requests.post(service_url, data={'msgId': message_id}, headers=headers)
# print(response)
# print(response.ok)
