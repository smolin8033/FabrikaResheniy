from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    CharField,
    DateTimeField,
    SerializerMethodField,
)

from message.models import Message
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


class MailingListSerializer(ModelSerializer):
    """
    Сериалайзер для просмотра рассылок и количества
    отправленных сообщений с группировкой по статусам
    """

    start_datetime = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    message_text = CharField(read_only=True)
    end_datetime = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    filter_field = MailingFilterSerializer(read_only=True)
    # messages_sent = SerializerMethodField(read_only=True, default=0)
    # messages_not_sent = SerializerMethodField(read_only=True, default=0)
    msg_status_true_count = IntegerField(read_only=True)
    msg_status_false_count = IntegerField(read_only=True)

    class Meta:
        model = Mailing
        fields = (
            "id",
            "start_datetime",
            "message_text",
            "end_datetime",
            "filter_field",
            "msg_status_true_count",
            "msg_status_false_count",
        )

    @staticmethod
    def get_messages_sent(instance):
        number_of_messages_sent = Message.objects.filter(mailing=instance, status=True).count()
        return number_of_messages_sent

    @staticmethod
    def get_messages_not_sent(instance):
        number_of_messages_not_sent = Message.objects.filter(mailing=instance, status=False).count()
        return number_of_messages_not_sent


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
        fields = ("id", "start_datetime", "message_text", "end_datetime", "filter_field")


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
        fields = ("id", "start_datetime", "message_text", "end_datetime", "filter_field")
