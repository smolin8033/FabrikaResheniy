from django.utils import timezone

from services.create_messages import create_messages
from services.filter_customers import filter_customers


def check_conditions(mailing):
    """
    Проверяет два условия, чтобы создать и выслать сообщения, если True
    """

    time_checked = check_time(mailing)
    customers_checked = check_customers(mailing)
    if time_checked and customers_checked:
        create_messages(mailing, customers_checked)
    return False


def check_time(mailing):
    return mailing.start_datetime <= timezone.localtime() <= mailing.end_datetime


def check_customers(mailing):
    """
    Проверяет, если ли клиенты, которым выслать сообщения после фильтрации клиентов
    """
    customers = filter_customers(mailing)
    return customers
