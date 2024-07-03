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


class UpdateRestaurant(BaseModel):
    restaurant_name: str
    restaurant_email: str
    phone_number: str
    rating: float


class UpdateRestaurantImages(BaseModel):
    logo: bytes
    background: bytes


class FoodAdd(BaseModel):
    kind: str
    price: float
    cook_time: int
    image: str
    food_name: str
    description: str
    restaurant_id: int


class UpdateFood(BaseModel):

    kind: str
    price: float
    cook_time: int
    image: str
    food_name: str
    description: str
    restaurant_id: int


