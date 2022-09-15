from factory import SubFactory
from faker import Faker
from factory.django import DjangoModelFactory


class MailingFilterFactory(DjangoModelFactory):
    """
    Фабрика для модели фильтра рассылки
    """

    faker = Faker()

    operator_code = int(faker.bothify(text="###"))
    tag = faker.word()


class MailingFactory(DjangoModelFactory):
    """
    Фабрика для модели рассылки
    """

    faker = Faker()

    start_datetime = faker.date_time_this_month()
    end_datetime = faker.future_datetime()
    message_text = faker.text()
    filter_field = SubFactory(MailingFilterFactory)
