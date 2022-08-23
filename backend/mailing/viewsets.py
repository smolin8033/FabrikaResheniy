from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.check_conditions import check_conditions
from services.serializer_validation_service import serialize_and_validate_mailing, serialize_and_validate_filter

from .models import Mailing
from .serializers import MailingSerializer


@extend_schema(tags=['Рассылки'])
class MailingViewSet(ModelViewSet):
    """
    Вьюсет для Рассылки
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        mailing_serializer = serialize_and_validate_mailing(request)

        filter_serializer = serialize_and_validate_filter(mailing_serializer)

        self.perform_create(mailing_serializer, filter_serializer=filter_serializer)
        headers = self.get_success_headers(mailing_serializer.data)
        return Response(mailing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())

        check_conditions(mailing)

    def update(self, request, *args, **kwargs):
        mailing_serializer = serialize_and_validate_mailing(request)

        filter_serializer = serialize_and_validate_filter(mailing_serializer)

        self.perform_update(mailing_serializer, filter_serializer=filter_serializer)
        return Response(mailing_serializer.data)

    def perform_update(self, serializer, *args, **kwargs):
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())

        check_conditions(mailing)
"""
передать instance и validated_data и просто сохранить объект
"""
