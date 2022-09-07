from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    BooleanField,
    CharField,
    ReadOnlyField,
)

from .models import Message


class MessageListSerializer(ModelSerializer):
    message_id = ReadOnlyField(source="id")
    created_at = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    status = BooleanField(read_only=True)
    mailing_text = CharField(read_only=True, source="mailing.message_text")
    customer_phone = CharField(read_only=True, source="customer.phone_number")

    class Meta:
        model = Message
        fields = ("message_id", "created_at", "status", "mailing_text", "customer_phone")
