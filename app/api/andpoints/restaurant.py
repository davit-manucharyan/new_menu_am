from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse

from app import main
from app.core import security
from app.schemas.shemas import RestaurantAdd, UpdateRestaurant


restaurant_router = APIRouter(tags=["restaurant"], prefix="/restaurant")


@restaurant_router.post("/add_restaurant")
def add_restaurant(data: RestaurantAdd):
    try:
        main.cursor.execute("""INSERT INTO comments (restaurant_name, restaurant_email, phone_number,
                                address, rating, background_image, logo) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (data.restaurant_name, data.restaurant_email,
                             data.phone_number, data.address, data.rating, data.logo,
                             data.background_image))

        main.conn.commit()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant successfully added"})


@restaurant_router.put("/update_restaurant/{restaurant_id}")
def update_restaurant(restaurant_id: int, data: UpdateRestaurant):
    try:
        main.cursor.execute("""SELECT * FROM restaurants WHERE restaurant_id= %s""",
                            (restaurant_id,))

        target_restaurant = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Restaurant not found")

    try:
        main.cursor.execute("""UPDATE comments SET  restaurant_name=%s, restaurant_email=%s, phone_number=%s,
                            rating=%s, logo=%s, background_image=%s   WHERE comment_id = %s AND user_id = %s""",
                            (data.restaurant_name, data.restaurant_email, data.phone_number,
                             data.rating, data.logo, data.background_image))

        main.conn.commit()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant updated successfully"})


@restaurant_router.delete("/delete_restaurant/{restaurant_id}")
def delete_post(restaurant_id: int):
    try:
        main.cursor.execute("""SELECT * FROM restaurants WHERE restaurant_id= %s""",
                            (restaurant_id,))

        target_restaurant = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Restaurant not found")

    main.cursor.execute("""DELETE FROM restaurants WHERE restaurant_id=%s""",
                        (restaurant_id,))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant successfully deleted"})


@restaurant_router.get("/get_restaurant_by_id/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    try:
        main.cursor.execute("""SELECT * FROM restaurants WHERE restaurant_id=%s""",
                            (restaurant_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No restaurant found with {restaurant_id} ids"
                                   f"ERROR: {error}")

    try:
        restaurant = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while searching for the restaurant"
                            f"ERROR: {error}")

    if restaurant is None:
        raise HTTPException(status_code=404,
                            detail=f"Restaurant with id {restaurant_id} was not found!")

    return restaurant
