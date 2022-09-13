import pytest
from django.urls import reverse
from rest_framework import status

from tests.conftest import api_client


class TestCustomerViewSet:
    """
    Тестирование API клиента
    """

    @pytest.mark.django_db
    def test_action_create_no_operator_code(self, customer_factory):
        data = {"phone_number": "Номер телефона", "tag": "Тег"}
        url = reverse("customers_list")
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        # print(customer_factory.phone_number)
        # assert True
