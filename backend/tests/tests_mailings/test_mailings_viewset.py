import pytest
from django.urls import reverse
from rest_framework import status

from mailing.models import Mailing, MailingFilter
from tests.tests_mailings.factories.mailing_factory import MailingFactory


class TestMailingFilterViewSet:
    @pytest.mark.django_db
    def test_action_create_no_messages(self, api_client):
        data = {
            "start_datetime": "2022-08-16 12:05:00",
            "message_text": "message_textmessage_textmessage_text",
            "end_datetime": "2050-08-16 12:05:00",
            "filter_field": {"operator_code": 920, "tag": "random_tag"},
        }
        url = reverse("mailings-list")

        assert Mailing.objects.count() == 0

        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Mailing.objects.count() == 1

    @pytest.mark.django_db
    def test_action_delete(self, api_client):
        mailing = MailingFactory()
        url = reverse("mailings-detail", kwargs={"pk": mailing.pk})

        assert Mailing.objects.count() == 1
        assert MailingFilter.objects.count() == 1

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Mailing.objects.count() == 0
        assert MailingFilter.objects.count() == 0
