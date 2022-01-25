import logging

import requests

from app.conf import EMAIL_SERVICE_API
from app.models import UserModel


def send_activation_email(user: UserModel) -> bool:
    """
    Sends activation email to the user's email. Logging in console the activation code
    :param user:
    :return:
    """
    url = 'send_email/'
    data = {
        'receiver': user.email,
        'subject': 'User registration email',
        'message': 'Dear, {}, \nYour activation code is: {}'.format(user.email, user.activation_code)
    }
    logging.info('Trying to send email to {} with activation code {}'.format(user.email, user.activation_code))
    try:
        response = requests.post(EMAIL_SERVICE_API + url, json=data)
        if not 200 <= response.status_code < 300:
            logging.warning('Email could not be sent due to server issues'.format(str(response.json())))

    except Exception as exception:
        logging.error('Email could not be sent due to: {}'.format(str(exception)))
        return False

    return True
