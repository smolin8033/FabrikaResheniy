import uuid
from django.db import models


class Mailing(models.Model):
    """
    Рассылка
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время рассылки')
    message_text = models.TextField()
    # фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.message_text[:50]
