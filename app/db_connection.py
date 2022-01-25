from typing import Optional

import psycopg2

from app.models import UserModel

from app.conf import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def initialize_database() -> None:
    """
    Initializes the database - only if database doesn't exists
    :return: None
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cur = connection.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Users "
            "(email varchar PRIMARY KEY, "
            "password varchar, "
            "activation_code varchar, "
            "activation_code_expiry timestamp, "
            "activated bool, "
            "activation_retries integer)")


def get_user_by_email_and_pass(email: str, password: str) -> Optional[UserModel]:
    """
    Returns a user by email and password or None if it's not found
    :param email: str
    :param password: str
    :return: Optional[UserModel]
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT email, activated, activation_code, activation_code_expiry, activation_retries "
            "FROM Users WHERE email = %s and password = %s", (
                email, password))
        result = cursor.fetchone()
        if not result:
            return None

        return UserModel(email=result[0],
                         activated=result[1],
                         activation_code=result[2],
                         activation_code_expiration=result[3],
                         activation_retries=result[4],
                         )


def check_email_exists(email: str) -> bool:
    """
    Checks in the database if the email already exits or not
    :param email: str
    :return: bool
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "select email from users where email = %s", (email,))

        if cursor.fetchone():
            return True

        return False


def insert_user(user: UserModel) -> None:
    """
    Insert user in database
    :param user: UserModel
    :return: None
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Users (email, password, activation_code, activation_code_expiry, "
            "activated, activation_retries) "
            "VALUES (%s, %s, %s, %s, %s, %s)", (
                user.email, user.password, user.activation_code, user.activation_code_expiration, user.activated,
                user.activation_retries))
        connection.commit()


def update_retries_on_user(user: UserModel) -> None:
    """
    Updates the number of retries of an user
    :param user: UserModel
    :return: None
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Users SET activation_retries = activation_retries + 1 where email = %s", (user.email,))
        connection.commit()


def update_activate_user(user: UserModel) -> None:
    """
    Updates the activated field to true, and the other activation related fields to null for a user
    :param user: UserModel
    :return: None
    """
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Users SET activated = True, activation_code=null, activation_code_expiry=null, "
            "activation_retries=null  where email = %s", (
                user.email,))
        connection.commit()
