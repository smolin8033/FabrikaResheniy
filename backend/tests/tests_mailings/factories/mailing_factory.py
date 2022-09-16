from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from mailing.models import MailingFilter, Mailing

faker = Faker()


class MailingFilterFactory(DjangoModelFactory):
    """
    Фабрика для модели фильтра рассылки
    """

    operator_code = int(faker.bothify(text="###"))
    tag = faker.word()

    class Meta:
        model = MailingFilter


class MailingFactory(DjangoModelFactory):
    """
    Фабрика для модели рассылки
    """

    start_datetime = faker.date_time_this_month()
    end_datetime = faker.future_datetime()
    message_text = faker.text()
    filter_field = SubFactory(MailingFilterFactory)

    class Meta:
        model = Mailing
