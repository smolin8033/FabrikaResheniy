from factory import Sequence
from factory.django import DjangoModelFactory

from customer.models import Customer


class CustomerFactory(DjangoModelFactory):
    """
    Фабрика для модели клиента
    """

    phone_number = Sequence(lambda n: f"7916575293{n}")
    tag = "1tag"
    # username = factory.Sequence(lambda n: 'john%s' % n)

    class Meta:
        model = Customer
