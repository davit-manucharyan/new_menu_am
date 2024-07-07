from sqlalchemy import Column, Integer, String, ForeignKey, text, Float, ARRAY, LargeBinary, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP, Time

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    status = Column(Boolean, nullable=True, server_default="False")
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Card(Base):
    __tablename__ = "cards"

    card_id = Column(Integer, nullable=False, primary_key=True)
    card_number = Column(Integer, nullable=False)
    card_valid_thru = Column(String, nullable=False)  # "MM/YYYY"
    card_name = Column(String, nullable=False)
    card_cvv = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, nullable=False, primary_key=True)
    address_to = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    food_id = Column(Integer, ForeignKey("foods.food_id"))


class FavoriteFood(Base):
    __tablename__ = "favorite_foods"

    favorite_food_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    food_id = Column(Integer, ForeignKey("foods.food_id"))


class Food(Base):
    __tablename__ = "foods"

    food_id = Column(Integer, nullable=False, primary_key=True)
    kind = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    cook_time = Column(Integer, nullable=False)
    image = Column(String, nullable=False)
    food_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))


class WorkTime(Base):
    __tablename__ = "work_time"

    work_time_id = Column(Integer, nullable=False, primary_key=True)
    day_of_week = Column(String, nullable=False)
    opening_time = Column(String, nullable=False)
    closing_time = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))


class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, nullable=False, primary_key=True)
    restaurant_name = Column(String, nullable=False)
    restaurant_email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    background_image = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

