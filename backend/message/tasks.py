import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from message.models import Message
from message.services.send_messages_service import send_message

logger = get_task_logger(__name__)


@shared_task
def send_messages(messages_ids):
    """
    Отправка сообщений
    """
    logger.debug(messages_ids)
    for msg_id in messages_ids:
        send_message(msg_id)


@shared_task
def send_not_sent_message():
    """
    Отправка неотправленных сообщений
    """
    messages_ids = Message.objects.filter(
        status=False, mailing__end_datetime__gte=datetime.datetime.now()
    ).values_list("id", flat=True)

    for msg_id in messages_ids:
        send_message(msg_id)
