from fastapi import HTTPException, status, APIRouter, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
import os
import shutil
import main
import datetime

from schemas.shemas import UpdateRestaurant

restaurant_router = APIRouter(tags=["restaurant"], prefix="/restaurant")


@restaurant_router.post("/add_restaurant")
def add_restaurant(restaurant_name: str = Form(...), restaurant_email: str = Form(...), phone_number: str = Form(...),
                   address: str = Form(...), rating: float = Form(), image_logo: UploadFile = File(...),
                   image_background: UploadFile = File(...)):

    current_date_time = (datetime.datetime.now().strftime('%B %d %Y - %H_%M_%S'))
    image_logo_url = f"{os.getcwd()}/static/images/logo/{current_date_time}{image_logo.filename}"
    image_background_url = f"{os.getcwd()}/static/images/background/{current_date_time}{image_background.filename}"

    try:

        main.cursor.execute("""INSERT INTO restaurants (restaurant_name, restaurant_email, phone_number,
                                        address, rating, background_image, logo) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (restaurant_name, restaurant_email,
                             phone_number, address, rating, image_background_url,
                             image_logo_url))

        main.conn.commit()

        with open(image_logo_url, "wb") as file_object:

            shutil.copyfileobj(image_logo.file, file_object)

        with open(image_background_url, "wb") as file_object:

            shutil.copyfileobj(image_background.file, file_object)

    except Exception as error:
        main.conn.rollback()
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
        main.cursor.execute("""UPDATE restaurants SET  restaurant_name=%s, restaurant_email=%s, 
                            phone_number=%s, rating=%s   
                            WHERE restaurant_id = %s""",
                            (data.restaurant_name, data.restaurant_email, data.phone_number,
                             data.rating, restaurant_id))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant updated successfully"})


@restaurant_router.put("/update_images_restaurants/{restaurant_id}")
def update_images(restaurant_id, image_logo: UploadFile = File(...), image_background: UploadFile = File(...)):

    current_date_time = (datetime.datetime.now().strftime('%B %d %Y - %H_%M_%S'))
    image_logo_url = f"{os.getcwd()}/static/images/logo/{current_date_time}{image_logo.filename}"
    image_background_url = f"{os.getcwd()}/static/images/background/{current_date_time}{image_background.filename}"

    try:
        main.cursor.execute("""UPDATE restaurants SET  logo = %s, background_image = %s   
                                   WHERE restaurant_id = %s""",
                            (image_logo_url, image_background_url, restaurant_id))

        main.conn.commit()

        with open(image_logo_url, "wb") as file_object:

            shutil.copyfileobj(image_logo.file, file_object)

        with open(image_background_url, "wb") as file_object:

            shutil.copyfileobj(image_background.file, file_object)

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant images updated successfully"})


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

    try:
        main.cursor.execute("""DELETE FROM restaurants WHERE restaurant_id=%s""",
                            (restaurant_id,))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Restaurant successfully deleted"})


@restaurant_router.get("/get_restaurant_by_id/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: int):
    try:
        main.cursor.execute("""SELECT * FROM restaurants WHERE restaurant_id=%s""",
                            (restaurant_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No restaurant found with {restaurant_id} id"
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


@restaurant_router.get("/get_all_restaurants")
def get_all_restaurants(page: int = Query(default=1, ge=1)):
    per_page = 20

    main.cursor.execute("SELECT count(*) FROM restaurants")
    count = main.cursor.fetchone()['count']
    if count == 0:
        return []

    max_page = (count - 1) // per_page + 1

    if page > max_page:
        page = max_page

    offset = (page - 1) * per_page

    try:
        main.cursor.execute("SELECT * FROM restaurants LIMIT %s OFFSET %s", (per_page, offset))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": str(error)})

    try:
        restaurants = main.cursor.fetchall()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while searching for all restaurants. ERROR: {str(error)}")

    if not restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Restaurants were not found!")

    return {
        "restaurants": restaurants,
        "page": page,
        "total_pages": max_page,
        "total_restaurants": count
    }
