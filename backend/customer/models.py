import pytz
from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number_regex = RegexValidator(regex=r'^7\d{10}$')
    phone_number = models.CharField(validators=[phone_number_regex], max_length=11, unique=True)
    operator_code = models.IntegerField()
    # тег (произвольная метка
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def __str__(self):
        return self.phone_number
