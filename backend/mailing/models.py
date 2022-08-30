from django.db import models


class MailingFilter(models.Model):
    """
    Модель для фильтра свойств клиентов (код оператора, тег),
    на которых должна быть произведена рассылка
    """
    operator_code = models.IntegerField(verbose_name='Код оператора')
    tag = models.CharField(verbose_name='Тег', max_length=50, blank=True)

    def __str__(self):
        return f'Код: {self.operator_code}, тег: {self.tag}'


class Mailing(models.Model):
    """
    Рассылка
    """
    start_datetime = models.DateTimeField(verbose_name='Время старта рассылки')
    message_text = models.TextField(verbose_name='Текст сообщения')
    filter_field = models.ForeignKey(MailingFilter, verbose_name='Фильтрация', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    end_datetime = models.DateTimeField(verbose_name='Время окончания рассылки')

    def __str__(self):
        return self.message_text[:50]

    def delete(self, *args, **kwargs):
        MailingFilter.objects.filter(mailing=self).delete()
        super(Mailing, self).delete(*args, **kwargs)
