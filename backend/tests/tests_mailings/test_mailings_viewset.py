import pytest
import requests
from django.urls import reverse
from rest_framework import status

from mailing.models import Mailing, MailingFilter
from message.tasks import send_messages
from services.check_conditions import check_time, check_conditions
from tests.tests_customers.factories.customer_factory import CustomerFactory
from tests.tests_mailings.factories.mailing_factory import MailingFactory
from tests.tests_mailings.mocks import fake_check_time, fake_requests_post


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
    def test_action_create_with_messages_status_True(self, api_client, monkeypatch):
        """
        ***
        """

        CustomerFactory(operator_code=920, tag="random_tag")
        data = {
            "start_datetime": "2022-08-16 12:05:00",
            "message_text": "message_textmessage_textmessage_text",
            "end_datetime": "2050-08-16 12:05:00",
            "filter_field": {"operator_code": 920, "tag": "random_tag"},
        }
        url = reverse("mailings-list")
        monkeypatch.setattr(send_messages, "delay", send_messages.run)
        monkeypatch.setattr(requests, "post", fake_requests_post)
        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Mailing.objects.count() == 1
        mailing = Mailing.objects.first()
        message = mailing.message_set.first()
        assert message.status is True

    @pytest.mark.django_db
    def test_action_create_with_messages_status_False(self, api_client, monkeypatch):
        """
        ***
        """

        CustomerFactory(operator_code=920, tag="random_tag")
        data = {
            "start_datetime": "2022-08-16 12:05:00",
            "message_text": "message_textmessage_textmessage_text",
            "end_datetime": "2050-08-16 12:05:00",
            "filter_field": {"operator_code": 920, "tag": "random_tag"},
        }
        url = reverse("mailings-list")
        monkeypatch.setattr(send_messages, "delay", send_messages.run)
        monkeypatch.setattr(fake_requests_post, "status", False, raising=False)
        monkeypatch.setattr(requests, "post", fake_requests_post)
        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Mailing.objects.count() == 1
        mailing = Mailing.objects.first()
        message = mailing.message_set.first()
        assert message.status is False

    # monkeypatch.setattr(check_conditions, "check_time", fake_check_time)

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
        messages_false = [MessageFactory(mailing=mailing, status=False) for _ in range(2)]

        url = reverse("mailings")
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert len(res_json) == 1
        assert res_json[0]["msg_sent_count"] == 3
        assert res_json[0]["msg_not_sent_count"] == 2
