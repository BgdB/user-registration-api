from datetime import datetime, timedelta

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import conf, db_connection, helper
from app.models import UserModel, ActivationModel
from app.email_service import send_activation_email
from app.helper import generate_activation_code

app = FastAPI()

security = HTTPBasic()


@app.post("/register")
def register(user: UserModel):
    """
    Register user api method
    :param user: UserModel
    :return:
    """
    if db_connection.check_email_exists(user.email):
        raise HTTPException(status_code=400, detail=conf.EXISTENT_USER_EXCEPTION_MESSAGE)

    if not helper.valid_email(user.email):
        raise HTTPException(status_code=400, detail=conf.WRONG_EMAIL_FORMAT_EXCEPTION_MESSAGE)

    if not helper.valid_password(user.password):
        raise HTTPException(status_code=400,
                            detail=conf.UNSECURE_PASSWORD_EXCEPTION_MESSAGE)

    user.password = helper.encrypt_string(user.password)
    user.activation_code = generate_activation_code()
    user.activation_code_expiration = datetime.now() + timedelta(minutes=1)
    db_connection.insert_user(user)
    send_activation_email(user)

    return {"message": "User registration successful"}


@app.post("/activate")
def activate(activation: ActivationModel, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Activate user api method
    :param activation: ActivationModel
    :param credentials: HTTPBasicCredentials
    :return:
    """
    now = datetime.now()  # getting it before db connection to be more accurate
    user = db_connection.get_user_by_email_and_pass(credentials.username, helper.encrypt_string(credentials.password))
    if not user:
        raise HTTPException(status_code=404, detail=conf.USER_NOT_FOUND_EXCEPTION_MESSAGE)

    if user.activated:
        raise HTTPException(status_code=403, detail=conf.USER_ALREADY_ACTIVE_EXCEPTION_MESSAGE)

    if user.activation_retries >= conf.MAX_RETRIES:
        raise HTTPException(status_code=403, detail=conf.MULTIPLE_ATTEMPTS_EXCEPTION_MESSAGE)

    db_connection.update_retries_on_user(user)
    if user.activation_code != activation.code:
        raise HTTPException(status_code=403, detail=conf.INCORRECT_ACTIVATION_CODE_EXCEPTION_MESSAGE)

    if user.activation_code_expiration < now:
        raise HTTPException(status_code=403, detail=conf.EXPIRED_ACTIVATION_CODE_EXCEPTION_MESSAGE)

    db_connection.update_activate_user(user)
    return {"message": "User activation successful"}


if __name__ == "__main__":
    db_connection.initialize_database()
    uvicorn.run(app, host="0.0.0.0", port=8000)
