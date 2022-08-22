import datetime

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from customer.models import Customer
from message.models import Message
from message.tasks import send_messages
from .models import Mailing
from .serializers import MailingSerializer, MailingFilterSerializer


@extend_schema(tags=['Рассылки'])
class MailingViewSet(ModelViewSet):
    """
    Вьюсет для Рассылки
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filter_data = serializer.validated_data.pop('filter_field')

        filter_serializer = MailingFilterSerializer(data=filter_data)
        filter_serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, filter_serializer=filter_serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())

        self.check_time(mailing)

    def check_time(self, mailing):
        if mailing.start_datetime <= timezone.localtime() <= mailing.end_datetime:
            self.check_customers(mailing)

    def check_customers(self, mailing):
        customers = self.filter_customers(mailing)
        if customers:
            self.create_messages(mailing, customers)

    @staticmethod
    def filter_customers(mailing):
        customers = Customer.objects.filter(
            operator_code=mailing.filter_field.operator_code,
            tag=mailing.filter_field.tag
        )
        return customers

    @staticmethod
    def create_messages(mailing, customers):
        messages = []
        for customer in customers:
            messages.append(Message(
                created_at=datetime.datetime.now(),
                mailing=mailing,
                customer=customer
            ))

        messages = Message.objects.bulk_create(messages)
        messages_ids = [message.id for message in messages]
        send_messages.delay(messages_ids)
