import json
import requests

from django.db import transaction
from django.shortcuts import get_object_or_404

from message.models import Message


def send_message(msg_id):
    """Сервис для отправки сообщений"""

    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI6ImZhYnJ"
        "pcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo"
    )
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"id": msg_id, "phone": 0, "text": "string"}
    service_url = f"https://probe.fbrq.cloud/v1/send/{msg_id}"
    response = requests.post(service_url, headers=headers, data=json.dumps(data))

    if response.ok:
        message = get_object_or_404(Message, id=msg_id)
        with transaction.atomic():
            message.status = True
            message.save(update_fields=["status"])
