import unittest
from unittest.mock import patch

from app import email_service
from app.models import UserModel


class EmailServiceTest(unittest.TestCase):
    class Response:
        status_code: str

    @patch('app.email_service.requests')
    def test_success(self, mock_requests):
        user = UserModel(email="dummy@email.com", activation_code='0123')
        response_object = self.Response()
        response_object.status_code = 200
        mock_requests.post.return_value = response_object
        response = email_service.send_activation_email(user)

        assert response is True

    @patch('app.email_service.requests')
    def test_service_not_available(self, mock_requests):
        user = UserModel(email="dummy@email.com", activation_code='0123')
        mock_requests.post.side_effect = Exception("Service Down")
        response = email_service.send_activation_email(user)

        assert response is False
