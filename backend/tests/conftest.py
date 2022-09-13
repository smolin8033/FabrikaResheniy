import pytest

from rest_framework.test import APIClient
from tests.tests_customers.factories.customer_factory import CustomerFactory
from pytest_factoryboy import register

register(CustomerFactory)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
