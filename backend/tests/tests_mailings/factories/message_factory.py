from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from message.models import Message
from tests.tests_customers.factories.customer_factory import CustomerFactory
from tests.tests_mailings.factories.mailing_factory import MailingFactory

faker = Faker()


class MessageFactory(DjangoModelFactory):
    """
    Фабрика для модели сообщений
    """

    created_at = faker.date_time_this_month()
    mailing = SubFactory(MailingFactory)
    customer = SubFactory(CustomerFactory)

    class Meta:
        model = Message
