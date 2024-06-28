# For Data Validations
from pydantic import BaseModel, EmailStr


class UserAdd(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    name: str
    email: EmailStr
    # main_photo: bytes


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordReset(BaseModel):
    new_password: str
    mail: str
    confirm_password: str


