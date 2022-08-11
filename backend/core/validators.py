from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(regex=r'^7\d{10}$')
