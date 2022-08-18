import uuid

from django.db import models


class Message(models.Model):
    """
    Сообщение
    """
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус', default=False)
    mailing = models.ForeignKey('mailing.Mailing', verbose_name='Отправлено в рамках рассылки:',
                                on_delete=models.CASCADE)
    customer = models.ForeignKey('customer.Customer', verbose_name='Отправлено клиенту:', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mailing)
