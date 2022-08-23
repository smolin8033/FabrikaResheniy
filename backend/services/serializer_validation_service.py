from mailing.serializers import MailingSerializer, MailingFilterSerializer


def serialize_and_validate_mailing(request):
    serializer = MailingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize_and_validate_filter(mailing_serializer):
    filtered_data = mailing_serializer.validated_data.pop('filter_field')

    filter_serializer = MailingFilterSerializer(data=filtered_data)
    filter_serializer.is_valid(raise_exception=True)

    return filter_serializer
