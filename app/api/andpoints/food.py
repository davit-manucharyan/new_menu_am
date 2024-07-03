from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse

import main

from schemas.shemas import FoodADD, UpdateFood

food_router = APIRouter(tags=["food"], prefix="/food")


@food_router.post("/add_food/{restaurant_id}")
def add_restaurant(data: FoodADD, restaurant_id: int):
    try:
        main.cursor.execute("""INSERT INTO foods (kind, price, cook_time,
                        image, food_name, descrition, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (data.kind, data.price, data.cook_time, data.image,
                             data.food_name, data.description, restaurant_id))

        main.conn.commit()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food successfully added"})


@food_router.put("/update_food/{food_id}")
def update_food(food_id: int, data: UpdateFood):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id= %s""",
                            (food_id,))

        target_food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    try:
        main.cursor.execute("""UPDATE restaurants SET  restaurant_name=%s, restaurant_email=%s, 
                            phone_number=%s, rating=%s, logo=%s, background_image=%s   
                            WHERE restaurant_id = %s""",
                            (data.restaurant_name, data.restaurant_email, data.phone_number,
                             data.rating, data.logo, data.background_image, restaurant_id))

        main.conn.commit()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant updated successfully"})


@restaurant_router.delete("/delete_restaurant/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
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

