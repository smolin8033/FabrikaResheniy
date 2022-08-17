from rest_framework.serializers import ModelSerializer

from .models import Mailing


class MailingSerializer(ModelSerializer):
    """
    Сериалайзер для модели Рассылки
    """
    class Meta:
        model = Mailing
        fields = '__all__'
