from django.db import models

from core.constants import TIMEZONES
from core.validators import phone_number_regex


class Customer(models.Model):
    """
    Клиент
    """
    phone_number = models.CharField(validators=[phone_number_regex], max_length=11, unique=True)
    operator_code = models.IntegerField()
    tag = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if self.operator_code is None:
            self.operator_code = int(self.phone_number[1:4])
        super().save(*args, **kwargs)
