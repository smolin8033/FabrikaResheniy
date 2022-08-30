import json

import requests

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI6ImZhYnJ' \
            'pcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    for message_id in messages_ids:
        data = {
            'id': message_id,
            'phone': 0,
            'text': 'string'
        }
        service_url = f'https://probe.fbrq.cloud/v1/send/{message_id}'
        response = requests.post(service_url, headers=headers, data=json.dumps(data))
# response = requests.post(service_url, data={'msgId': message_id}, headers=headers)
# print(response)
# print(response.ok)
