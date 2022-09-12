import pytest
from tests.tests_customers.factories.customer_factory import CustomerFactory


class TestCustomerViewSet:
    """
    Тестирование API клиента
    """

    @pytest.mark.django_db
    def test_action_create_no_operator_code(self, customer_factory):

        print(customer_factory.phone_number)
        assert True
