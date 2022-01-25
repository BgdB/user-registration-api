from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    email: str
    password: str = None
    activation_code: Optional[str] = None
    activation_code_expiration: Optional[datetime]
    activation_retries: Optional[int] = 0
    activated: bool = False


class ActivationModel(BaseModel):
    code: str
