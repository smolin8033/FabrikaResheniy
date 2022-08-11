import uuid

from django.db import models


class Message(models.Model):
    """
    Сообщение
    """
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    # id рассылки, в рамках которой было отправлено данное сообщение
    # id клиента, которому отправили
    mailing = models.ForeignKey('mailing.Mailing', on_delete=models.CASCADE)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mailing)
