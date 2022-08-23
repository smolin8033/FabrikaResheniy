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

        filter_serializer = serialize_and_validate_filter(mailing_serializer)

        self.perform_create(mailing_serializer, filter_serializer=filter_serializer)
        headers = self.get_success_headers(mailing_serializer.data)
        return Response(mailing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, *args, **kwargs):
        mailing = serializer.save(filter_field=kwargs.get('filter_serializer').save())

        check_conditions(mailing)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
