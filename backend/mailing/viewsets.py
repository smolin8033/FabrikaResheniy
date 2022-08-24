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

        filter_serializer = serialize_and_validate_filter(request, mailing_serializer)

        self.perform_create(mailing_serializer, filter_serializer=filter_serializer)
        headers = self.get_success_headers(mailing_serializer.data)
        return Response(mailing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())

        check_conditions(mailing)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        mailing_serializer = serialize_and_validate_mailing(request, instance)
        filter_serializer = serialize_and_validate_filter(request, mailing_serializer, instance)

        self.perform_update(
            mailing_serializer,
            instance=instance,
            filter_serializer=filter_serializer
        )
        return Response(mailing_serializer.data)

    def perform_update(self, serializer, *args, **kwargs):
        """
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())
        не понимаю, почему не работает
        Правильно здесь работает? Не совсем понимаю, как должно правильно все обновляться
        """
        filter_serializer = kwargs.get('filter_serializer')
        instance = kwargs.get('instance')
        filter = instance.filter_field

        updated_filter = self.update_mailing_filter(filter, filter_serializer)
        updated_mailing = self.update_mailing_instance(instance, serializer, updated_filter)

        check_conditions(updated_mailing)

    def update_mailing_filter(self, filter, filter_serializer):
        filter.operator_code = filter_serializer.validated_data['operator_code']
        filter.tag = filter_serializer.validated_data['tag']

        filter.save()
        return filter

    def update_mailing_instance(self, instance, serializer, updated_filter):
        instance.start_datetime = serializer.validated_data['start_datetime']
        instance.message_text = serializer.validated_data['message_text']
        instance.filter_field = updated_filter
        instance.end_datetime = serializer.validated_data['end_datetime']

        instance.save()
        return instance


"""
передать instance и validated_data и просто сохранить объект

 OrderedDict([('start_datetime', datetime.datetime(2022, 8, 23, 18, 14, tzinfo=zoneinfo.ZoneInfo(key='Europe/Moscow'))), ('message_text', 'third_m
essagefirst_messagefirst_messagefirst_message'), ('end_datetime', datetime.datetime(2022, 8, 23, 20, 45, 2, tzinfo=zoneinfo.ZoneInfo(key='Europe/Moscow')))])

 OrderedDict([('operator_code', 916), ('tag', 'first_tag')])
"""
