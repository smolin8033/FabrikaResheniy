import logging

import pytest
from django.urls import reverse
from mailing.models import Mailing, MailingFilter
from rest_framework import status
from tests.tests_mailings.factories.mailing_factory import MailingFactory
from tests.tests_mailings.factories.message_factory import MessageFactory

log = logging.getLogger(__name__)


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

    @pytest.mark.django_db
    def test_action_list(self, api_client, django_assert_max_num_queries):
        mailing = MailingFactory()
        messages_true = [MessageFactory(mailing=mailing, status=True) for _ in range(3)]
        messages_false = [
            MessageFactory(mailing=mailing, status=False) for _ in range(2)
        ]

        url = reverse("mailings-list")
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 1
        assert json_response[0]["msg_sent_count"] == 3
        assert json_response[0]["msg_not_sent_count"] == 2

    @pytest.mark.django_db
    def test_action_mailing_with_messages(
        self, api_client, django_assert_max_num_queries
    ):
        mailing = MailingFactory()
        messages = [MessageFactory(mailing=mailing) for _ in range(3)]

        url = reverse("messages-mailing-info", kwargs={"pk": mailing.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 3
