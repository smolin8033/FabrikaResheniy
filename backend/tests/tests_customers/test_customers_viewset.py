import pytest
from django.urls import reverse
from rest_framework import status

from customer.models import Customer
from tests.tests_customers.factories.customer_factory import CustomerFactory


class TestCustomerViewSet:
    """
    Тестирование API клиента
    """

    @pytest.mark.django_db
    def test_action_create_no_operator_code(self, api_client):
        data = {"phone_number": "79165753429", "tag": "1tag"}
        url = reverse("customers-list")
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() == 1

        customer = Customer.objects.first()

        assert customer.phone_number == "79165753429"

    @pytest.mark.django_db
    def test_action_create_with_operator_code(self, api_client):
        data = {"phone_number": "79165753429", "tag": "1tag", "operator_code": 916}
        url = reverse("customers-list")
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() == 1

        customer = Customer.objects.first()

        assert customer.phone_number == "79165753429"

    @pytest.mark.django_db
    def test_action_update(self, api_client):
        customer = CustomerFactory()

        data = {"phone_number": "79165752934", "tag": "2tag"}
        url = reverse("customers-detail", kwargs={"pk": customer.pk})
        response = api_client.put(url, data=data)
        json_response = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json_response["phone_number"] != customer.phone_number
        assert json_response["tag"] != customer.tag
        assert json_response["timezone"] == customer.timezone
        assert json_response["operator_code"] == int(customer.operator_code)

    @pytest.mark.django_db
    def test_action_delete(self, api_client):
        # customers = [CustomerFactory() for _ in range(2)]
        customer = CustomerFactory()
        url = reverse("customers-detail", kwargs={"pk": customer.pk})

        assert Customer.objects.count() == 1

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Customer.objects.count() == 0

    @pytest.mark.django_db
    def test_action_list(self, api_client, django_assert_max_num_queries):
        url = reverse("customers-list")
        with django_assert_max_num_queries(1):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
