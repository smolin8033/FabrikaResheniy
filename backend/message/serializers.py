from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    BooleanField,
    CharField
)

from .models import Message


class MessageListSerializer(ModelSerializer):
    created_at = DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    status = BooleanField(read_only=True)
    mailing_text = CharField(read_only=True, source='mailing.message_text')
    customer_phone = CharField(read_only=True, source='customer.phone_number')

    class Meta:
        model = Message
        fields = (
            'id',
            'created_at',
            'status',
            'mailing_text',
            'customer_phone'
        )
