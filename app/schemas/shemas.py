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


class RestaurantAdd(BaseModel):
    restaurant_name: str
    restaurant_email: str
    phone_number: str
    address: str
    rating: float
    background_image: str
    logo: str


class UpdateRestaurant(BaseModel):
    restaurant_name: str
    restaurant_email: str
    phone_number: str
    rating: float
    background_image: str
    logo: str


class RestaurantWorkTimeAdd(BaseModel):
    restaurant_id: str
    day_of_week: str
    opening_time: str
    closing_time: str
