import requests

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI\
    6ImZhYnJpcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo'
    headers = {
        'Authorization': 'JWT {}'.format(token)
    }
    for message_id in messages_ids:
        service_url = f'https://probe.fbrq.cloud/v1/send/{message_id}/'
        response = requests.post(service_url, data={'msgId': message_id}, headers=headers)
        print(response)
        print('\n')
        print(response.ok)
# response = requests.post(service_url, data={'msgId': message_id}, headers=headers)
# print(response)
# print(response.ok)
