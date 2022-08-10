from django.db import models


class Mailing(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    message_text = models.TextField()
    # фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.message_text[:50]
