from pprint import pprint

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from services.check_conditions import check_conditions
from services.serializer_validation_service import (
    serialize_and_validate_mailing,
    serialize_and_validate_filter,
)

from .models import Mailing
from .serializers import MailingSerializer, MailingFilterSerializer


@extend_schema(tags=["Рассылки"])
class MailingViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """
    Вьюсет для Рассылки
    """

    queryset = Mailing.objects.select_related("filter_field").all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        mailing_serializer = serialize_and_validate_mailing(request)
        filter_serializer = serialize_and_validate_filter(request, mailing_serializer)
        self.perform_create(mailing_serializer, filter_serializer=filter_serializer)

        return Response(mailing_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(
        self, mailing_serializer: MailingSerializer, filter_serializer: MailingFilterSerializer
    ):
        filter = filter_serializer.save()
        mailing: Mailing = mailing_serializer.save(filter_field=filter)
        check_conditions(mailing)

    # @extend_schema(description="Метод обновления",
    #                parameters=[MailingSerializer]
    # )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        mailing_serializer = serialize_and_validate_mailing(request, instance)
        filter_serializer = serialize_and_validate_filter(request, mailing_serializer, instance)

        self.perform_update(
            mailing_serializer, instance=instance, filter_serializer=filter_serializer
        )
        return Response(mailing_serializer.data)

    def perform_update(self, mailing_serializer, *args, **kwargs):

        # не понимаю, почему не работает
        # Правильно здесь работает? Не совсем понимаю, как должно правильно все обновляться

        # filter_serializer = kwargs.get("filter_serializer")
        # instance = kwargs.get("instance")
        # filter_instance = instance.filter_field
        #
        # updated_filter = self.update_mailing_filter(filter_instance, filter_serializer)
        # updated_mailing = self.update_mailing_instance(instance, mailing_serializer, updated_filter)

        filter = kwargs.get("filter_serializer").save()
        mailing = mailing_serializer.save(filter_field=filter.id)
        print(filter.pk, mailing.pk)

        check_conditions(mailing)

    @staticmethod
    def update_mailing_filter(filter_instance, filter_serializer):
        filter_instance.operator_code = filter_serializer.validated_data["operator_code"]
        filter_instance.tag = filter_serializer.validated_data["tag"]

        filter_instance.save()
        return filter_instance

    @staticmethod
    def update_mailing_instance(instance, serializer, updated_filter):
        # instance.start_datetime = serializer.validated_data["start_datetime"]
        # instance.message_text = serializer.validated_data["message_text"]
        # instance.filter_field = updated_filter
        # instance.end_datetime = serializer.validated_data["end_datetime"]
        # instance.save()
        instance.__dict__.update(**serializer.validated_data, filter_field=updated_filter)
        instance.save()

        return instance
