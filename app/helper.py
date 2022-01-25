import hashlib
import random
import re


def generate_activation_code() -> str:
    """
    Generate 4 digit activation code
    :return: str
    """
    return "{}{}{}{}".format(random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))


def valid_email(email: str) -> bool:
    """
    Check if a email is valid or not
    :param email: str
    :return: bool
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True

    return False


def valid_password(password: str) -> bool:
    """
    Check if a password is strong enough
    :param password: str
    :return: bool
    """

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    return not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)


def encrypt_string(password: str) -> str:
    """
    Encrypts a string with sha256 algorithm
    :param password: str
    :return: str
    """
    sha_signature = hashlib.sha256(str(password).encode()).hexdigest()

    return sha_signature
