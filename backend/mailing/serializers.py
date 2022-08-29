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
        fields = (
            'operator_code',
            'tag'
        )


class MailingCreateSerializer(ModelSerializer):
    """
    Сериалайзер для создания модели Рассылки
    """
    start_datetime = DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    message_text = CharField(required=True)
    end_datetime = DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    filter_field = MailingFilterSerializer()

    class Meta:
        model = Mailing
        fields = (
            'id',
            'start_datetime',
            'message_text',
            'end_datetime',
            'filter_field'
        )


class MailingUpdateSerializer(ModelSerializer):
    """
    Сериалайзер для обновления модели Рассылки
    """
    start_datetime = DateTimeField(required=False, format="%Y-%m-%d %H:%M:%S")
    message_text = CharField(required=False)
    end_datetime = DateTimeField(required=False, format="%Y-%m-%d %H:%M:%S")
    filter_field = MailingFilterSerializer()

    class Meta:
        model = Mailing
        fields = (
            'id',
            'start_datetime',
            'message_text',
            'end_datetime',
            'filter_field'
        )
