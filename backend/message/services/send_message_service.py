import json

from django.contrib.sites import requests
from django.db import transaction
from django.shortcuts import get_object_or_404

from message.models import Message


def send_message(message_id: int):
    TOKEN = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE1MDI5MjIsImlzcyI6ImZhYnJ"
        "pcXVlIiwibmFtZSI6ImFsZXhzbTBsIn0.2XqlRn3_YsKz4w3EoBs_mQ5eY3ow7M3a4UqHKVGSxFo"
    )
    HEADERS = {"Authorization": "Bearer {}".format(TOKEN)}

    data = {"id": message_id, "phone": 0, "text": "string"}
    service_url = f"https://probe.fbrq.cloud/v1/send/{message_id}"
    response = requests.post(service_url, headers=HEADERS, data=json.dumps(data))
    if response.ok:
        message: Message = get_object_or_404(Message, id=message_id)
        with transaction.atomic():
            message.status = True
            message.save(update_fields=["status"])
