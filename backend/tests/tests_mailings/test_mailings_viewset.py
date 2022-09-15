import pytest

from tests.tests_mailings.factories.mailing_factory import MailingFilterFactory


class TestMailingFilterViewSet:
    @pytest.mark.django_db
    def test_action_create_no_operator_code(self, api_client):
        filter = MailingFilterFactory

        assert filter == MailingFilterFactory
