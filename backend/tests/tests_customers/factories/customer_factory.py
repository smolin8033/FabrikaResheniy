from customer.models import Customer
from factory import Sequence
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    """
    Фабрика для модели клиента
    """

    phone_number = Sequence(lambda n: f"7916575293{n}")
    tag = "1tag"

    class Meta:
        model = Customer
