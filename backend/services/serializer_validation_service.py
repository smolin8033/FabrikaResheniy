from mailing.serializers import MailingSerializer, MailingFilterSerializer


def serialize_and_validate_mailing(request, instance=None):
    serializer = MailingSerializer(data=request.data)
    if request.method == 'PUT':
        serializer = MailingSerializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)

    return serializer


def serialize_and_validate_filter(request, mailing_serializer, instance=None):
    filtered_data = mailing_serializer.validated_data.pop('filter_field')

    serializer = MailingFilterSerializer(data=filtered_data)
    if request.method == 'PUT':
        serializer = MailingFilterSerializer(instance, data=filtered_data)
    serializer.is_valid(raise_exception=True)

    return serializer
