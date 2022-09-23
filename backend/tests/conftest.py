import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from tests.tests_customers.factories.customer_factory import CustomerFactory

register(CustomerFactory)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
