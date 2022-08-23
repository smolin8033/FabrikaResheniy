from django.utils import timezone

from services.create_messages import create_messages
from services.filter_customers import filter_customers


def check_conditions(mailing):
    time_checked = check_time(mailing)
    customers_checked = check_customers(mailing)

    if time_checked and customers_checked:
        create_messages(mailing, customers_checked)
    return False


def check_time(mailing):
    return mailing.start_datetime <= timezone.localtime() <= mailing.end_datetime


def check_customers(mailing):
    customers = filter_customers(mailing)
    return customers
