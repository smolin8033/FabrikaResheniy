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

    # TODO with oper_code

    @pytest.mark.django_db
    def test_action_update_no_operator_code(self, api_client):
        customer = CustomerFactory()

        data = {"phone_number": "79165752934", "tag": "2tag"}
        url = reverse("customers-detail", kwargs={"pk": customer.pk})
        response = api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["phone_number"] != customer.phone_number
        assert response.json()["tag"] != customer.tag
        assert response.json()["timezone"] == customer.timezone
        assert response.json()["operator_code"] == int(customer.operator_code)

    # TODO количество нулю

    @pytest.mark.django_db
    def test_action_list(self, api_client, django_assert_max_num_queries):
        customers = [CustomerFactory() for _ in range(3)]
        url = reverse("customers-list")
        with django_assert_max_num_queries(0):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
