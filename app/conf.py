import logging
import os

logging.basicConfig(level=logging.INFO)
MAX_RETRIES = 3

DB_NAME = os.environ.get('POSTGRES_DB_NAME')
DB_USER = os.environ.get('POSTGRES_DB_USER')
DB_PASSWORD = os.environ.get('POSTGRES_DB_PASSWORD')
DB_HOST = os.environ.get('POSTGRES_DB_HOST')

EMAIL_SERVICE_API = os.environ.get('EMAIL_SERVICE_API')

EXISTENT_USER_EXCEPTION_MESSAGE = 'A user with this email already exits.'
WRONG_EMAIL_FORMAT_EXCEPTION_MESSAGE = 'Incorrect email format'
UNSECURE_PASSWORD_EXCEPTION_MESSAGE = 'Password must be at least 8 characters, contain at least one upper character, ' \
                                      'lower character, digit and special character'

USER_NOT_FOUND_EXCEPTION_MESSAGE = 'User/Password combination not found'
USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE = 'User already activated'
MULTIPLE_ATTEMPTS_EXCEPTION_MESSAGE = 'Account locked due to multiple activation attempts'
INCORRECT_ACTIVATION_CODE_EXCEPTION_MESSAGE = 'Incorrect activation code'
EXPIRED_ACTIVATION_CODE_EXCEPTION_MESSAGE = 'Activation code expired'
