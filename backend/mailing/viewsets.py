import datetime

from rest_framework.viewsets import ModelViewSet

from customer.models import Customer
from message.models import Message
from .models import Mailing
from .serializers import MailingSerializer


class MailingViewSet(ModelViewSet):
    """
    Вьюсет для Рассылки
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        mailing = serializer.save()

        self.filter_customers(mailing)

    def filter_customers(self, mailing):
        customers = Customer.objects.filter(
            operator_code=mailing.filter_field.operator_code,
            tag=mailing.filter_field.tag
        )

        self.create_messages(mailing, customers)
        return customers

    def create_messages(self, customers, mailing):
        messages = []
        for customer in customers:
            messages.append(Message(
                created_at=datetime.datetime.now(),
                mailing=mailing,
                customer=customer
            ))

        messages = Message.objects.bulk_create(messages)
        return messages
