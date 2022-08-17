import uuid
from django.db import models


class MailingFilter(models.Model):
    """
    Модель для фильтра свойств клиентов (код оператора, тег),
    на которых должна быть произведена рассылка
    """
    operator_code = models.IntegerField()
    tag = models.CharField(max_length=50, blank=True)


class Mailing(models.Model):
    """
    Рассылка
    """
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    start_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время рассылки')
    message_text = models.TextField()
    filter_field = models.ForeignKey(MailingFilter, blank=True, null=True, on_delete=models.SET_NULL)
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.message_text[:50]
