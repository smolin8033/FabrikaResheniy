from django.utils import timezone
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    CharField,
    DateTimeField,
)

from .models import Mailing, MailingFilter


class MailingFilterSerializer(ModelSerializer):
    """
    Сериалайзер для модели фильтрации свойств
    клиента (тег, код оператора)
    """

    operator_code = IntegerField()
    tag = CharField(required=True)

    class Meta:
        model = MailingFilter
        fields = ("operator_code", "tag")


class MailingSerializer(ModelSerializer):
    """
    Сериалайзер для модели Рассылки
    """

    start_datetime = DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    message_text = CharField(required=True)
    end_datetime = DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    filter_field = MailingFilterSerializer()

    class Meta:
        model = Mailing
        fields = ("id", "start_datetime", "message_text", "end_datetime", "filter_field")
