from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from mailing.models import Mailing
from message.models import Message
from message.serializers import MessageListSerializer


@extend_schema(tags=['Сообщения'])
class MessageViewSet(ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer

    @action(detail=False, methods=('GET',), url_path=r"mailing/(?P<pk>\w+)")
    def mailing_info(self, request, **kwargs):
        mailing = get_object_or_404(Mailing.objects.all(), pk=kwargs.get('pk'))
        messages = Message.objects.filter(mailing=mailing)
        serializer = self.get_serializer(messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)