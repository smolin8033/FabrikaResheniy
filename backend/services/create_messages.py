import datetime
import logging

from message.models import Message
from message.tasks import send_messages, send_not_sent_message

logger = logging.getLogger(__name__)


def create_messages(mailing, customers):
    """
    Создает сообщения и передает их в tasks для celery
    """
    messages = []
    for customer in customers:
        messages.append(
            Message(
                created_at=datetime.datetime.now(), mailing=mailing, customer=customer
            )
        )

    messages = Message.objects.bulk_create(messages)
    messages_ids = [message.id for message in messages]

    send_messages.delay(messages_ids)
