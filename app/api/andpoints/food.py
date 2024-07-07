from fastapi import HTTPException, status, APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import datetime
import os
import shutil
import main

from schemas.shemas import UpdateFood

food_router = APIRouter(tags=["food"], prefix="/food")


@food_router.post("/add_food/{restaurant_id}")
def add_food(restaurant_id: int, kind: str = Form(...), price: int = Form(...),
                   cook_time: int = Form(...), food_name: str = Form(...), description: str = Form(...),
                   image_food: UploadFile = File(...)):

    current_date_time = (datetime.datetime.now().strftime('%B %d %Y - %H_%M_%S'))
    image_food_url = f"{os.getcwd()}/static/images/food/{current_date_time}{image_food.filename}"

    try:
        main.cursor.execute("""INSERT INTO foods (kind, price, cook_time,
                        image, food_name, description, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (kind, price, cook_time, image_food_url,
                             food_name, description, restaurant_id))

        main.conn.commit()

        with open(image_food_url, "wb") as file_object:

            shutil.copyfileobj(image_food.file, file_object)

    except Exception as error:
        main.conn.rollback()
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
        main.cursor.execute("""UPDATE foods SET  kind=%s, price=%s, 
                            cook_time=%s, food_name=%s, description=%s   
                            WHERE food_id = %s""",
                            (data.kind, data.price, data.cook_time,
                             data.food_name, data.description, food_id))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food updated successfully"})


@food_router.put("/update_images_foods/{food_id}")
def update_images(food_id, image_food: UploadFile = File(...)):

    current_date_time = (datetime.datetime.now().strftime('%B %d %Y - %H_%M_%S'))
    image_food_url = f"{os.getcwd()}/static/images/food/{current_date_time}{image_food.filename}"


    try:
        main.cursor.execute("""UPDATE foods SET  image = %s   
                                   WHERE food_id = %s""",
                            (image_food_url, food_id))

        main.conn.commit()

        with open(image_food_url, "wb") as file_object:

            shutil.copyfileobj(image_food.file, file_object)

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food images updated successfully"})


@food_router.delete("/delete_food/{food_id}")
def delete_food(food_id: int):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id= %s""",
                            (food_id,))

        target_restaurant = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    try:
        main.cursor.execute("""DELETE FROM foods WHERE food_id=%s""",
                            (food_id,))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "There was an error deleting the food"
                                    f"ERROR: {error}"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food successfully deleted"})


@food_router.get("/get_food_by_id/{food_id}")
def get_food_by_id(food_id: int):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id=%s""",
                            (food_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No food found with {food_id} id"
                                   f"ERROR: {error}")

    try:
        food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while searching for the food"
                            f"ERROR: {error}")

    if food is None:
        raise HTTPException(status_code=404,
                            detail=f"Restaurant with id {food_id} was not found!")

    return food


@food_router.get("/get_all_foods")
def get_all_foods():
    try:
        main.cursor.execute("""SELECT * FROM foods""")

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    try:

        foods = main.cursor.fetchall()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while searching for all foods"
                            f"ERROR: {error}")

    if foods is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Foods were not found!")

    return foods

