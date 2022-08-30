from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.check_conditions import check_conditions
from services.serializer_validation_service import (
    serialize_and_validate_mailing,
    serialize_and_validate_filter
)

from .models import Mailing
from .serializers import MailingCreateSerializer, MailingFilterSerializer, MailingUpdateSerializer, \
    MailingListSerializer


@extend_schema(tags=['Рассылки'])
class MailingViewSet(ModelViewSet):
    """
    Вьюсет для Рассылки
    """
    def get_serializer_class(self):
        serializer_class = MailingCreateSerializer
        if self.action == 'list':
            serializer_class = MailingListSerializer
        return serializer_class

    def get_queryset(self):
        queryset = Mailing.objects.select_related('filter_field').all()
        return queryset

    @extend_schema(description='Создание рассылки')
    def create(self, request, *args, **kwargs):
        mailing_serializer = serialize_and_validate_mailing(request)

        filter_serializer = serialize_and_validate_filter(request, mailing_serializer)

        self.perform_create(mailing_serializer, filter_serializer=filter_serializer)
        headers = self.get_success_headers(mailing_serializer.data)
        return Response(mailing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, mailing_serializer, filter_serializer):
        filter_instance = filter_serializer.save()
        mailing = mailing_serializer.save(filter_field=filter_instance)

        check_conditions(mailing)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        mailing_serializer = serialize_and_validate_mailing(request, instance)
        filter_serializer = serialize_and_validate_filter(request, mailing_serializer, instance)

        self.perform_update(
            instance,
            mailing_serializer,
            filter_serializer
        )
        return Response(mailing_serializer.data)

    def perform_update(self, instance, mailing_serializer, filter_serializer):
        mailing_instance = instance
        filter_instance = mailing_instance.filter_field

        updated_filter = self.update_mailing_filter(filter_instance, filter_serializer)
        updated_mailing = self.update_mailing_instance(mailing_instance, mailing_serializer, updated_filter)

        check_conditions(updated_mailing)

    @staticmethod
    def update_mailing_filter(instance, filter_serializer):
        instance.__dict__.update(**filter_serializer.validated_data)
        instance.save()
        return instance

    @staticmethod
    def update_mailing_instance(instance, mailing_serializer, updated_filter):
        instance.__dict__.update(**mailing_serializer.validated_data, filter_field=updated_filter)
        instance.save()
        return instance
