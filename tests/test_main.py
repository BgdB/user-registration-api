import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

import main
from app import helper, conf
from app.models import UserModel, ActivationModel


class MainTest(unittest.TestCase):
    @patch('main.db_connection')
    @patch('main.send_activation_email')
    def test_register_success(self, mock_send_activation_email, mock_db_connection):
        user = UserModel(email='dummy@email.com', password='Passw0rd!')
        mock_db_connection.check_email_exists.return_value = False
        mock_send_activation_email.return_values = None
        response = main.register(user)
        mock_db_connection.insert_user.assert_called_with(user)

        self.assertEqual(user.password, helper.encrypt_string('Passw0rd!'))
        self.assertDictEqual(response, {'message': 'User registration successful'})

    @patch('main.db_connection')
    def test_register_fail_existent_email(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password='Passw0rd!')
        mock_db_connection.check_email_exists.return_value = True
        with self.assertRaises(HTTPException) as context:
            main.register(user)

        self.assertEqual(context.exception.detail, conf.EXISTENT_USER_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_register_fail_wrong_email_format(self, mock_db_connection):
        user = UserModel(email='dummy@email', password='Passw0rd!')
        mock_db_connection.check_email_exists.return_value = False
        with self.assertRaises(HTTPException) as context:
            main.register(user)

        self.assertEqual(context.exception.detail, conf.WRONG_EMAIL_FORMAT_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_register_fail_password_security(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password='Passw0rd')
        mock_db_connection.check_email_exists.return_value = False
        with self.assertRaises(HTTPException) as context:
            main.register(user)

        self.assertEqual(context.exception.detail, conf.UNSECURE_PASSWORD_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_activate_success(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password=helper.encrypt_string('Passw0rd!'), activation_code='1234',
                         activation_code_expiration=datetime.now() + timedelta(minutes=10), activation_retries=0,
                         activated=False)
        activation_obj = ActivationModel(code='1234')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = user
        response = main.activate(activation_obj, credentials_obj)
        mock_db_connection.insert_user.update_retries_on_user(user)
        mock_db_connection.insert_user.update_activate_user(user)

        self.assertEqual(user.password, helper.encrypt_string('Passw0rd!'))
        self.assertDictEqual(response, {'message': 'User activation successful'})

    @patch('main.db_connection')
    def test_activate_fail_wrong_email_or_password(self, mock_db_connection):
        activation_obj = ActivationModel(code='1234')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = None

        with self.assertRaises(HTTPException) as context:
            main.activate(activation_obj, credentials_obj)

        self.assertEqual(context.exception.detail, conf.USER_NOT_FOUND_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_activate_fail_user_already_active(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password=helper.encrypt_string('Passw0rd!'), activation_code='1234',
                         activation_code_expiration=datetime.now() + timedelta(minutes=10), activation_retries=0,
                         activated=True)
        activation_obj = ActivationModel(code='1234')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = user

        with self.assertRaises(HTTPException) as context:
            main.activate(activation_obj, credentials_obj)

        self.assertEqual(context.exception.detail, conf.USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_activate_max_retires_exceeded(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password=helper.encrypt_string('Passw0rd!'), activation_code='1234',
                         activation_code_expiration=datetime.now() + timedelta(minutes=10), activation_retries=3,
                         activated=True)
        activation_obj = ActivationModel(code='1234')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = user

        with self.assertRaises(HTTPException) as context:
            main.activate(activation_obj, credentials_obj)

        self.assertEqual(context.exception.detail, conf.USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_activate_incorrect_activation_code(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password=helper.encrypt_string('Passw0rd!'), activation_code='1234',
                         activation_code_expiration=datetime.now() + timedelta(minutes=10), activation_retries=0,
                         activated=True)
        activation_obj = ActivationModel(code='9999')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = user

        with self.assertRaises(HTTPException) as context:
            main.activate(activation_obj, credentials_obj)
        mock_db_connection.insert_user.update_retries_on_user(user)
        self.assertEqual(context.exception.detail, conf.USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE)

    @patch('main.db_connection')
    def test_activate_expired_activation_code(self, mock_db_connection):
        user = UserModel(email='dummy@email.com', password=helper.encrypt_string('Passw0rd!'), activation_code='1234',
                         activation_code_expiration=datetime.now() + timedelta(minutes=-1), activation_retries=0,
                         activated=True)
        activation_obj = ActivationModel(code='9999')
        credentials_obj = HTTPBasicCredentials(username='dummy@email.com', password='Passw0rd!')

        mock_db_connection.get_user_by_email_and_pass.return_value = user

        with self.assertRaises(HTTPException) as context:
            main.activate(activation_obj, credentials_obj)
        mock_db_connection.insert_user.update_retries_on_user(user)
        self.assertEqual(context.exception.detail, conf.USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE)
