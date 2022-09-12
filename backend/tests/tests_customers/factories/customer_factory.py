from factory import Faker
from factory.django import DjangoModelFactory

from customer.models import Customer


class CustomerFactory(DjangoModelFactory):
    """
    Фабрика для модели клиента
    """

    phone_number = Faker("phone_number")
    tag = "1tag"

    class Meta:
        model = Customer
