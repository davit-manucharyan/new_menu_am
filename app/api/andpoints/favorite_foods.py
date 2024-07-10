from fastapi import HTTPException, status, APIRouter, Query
from fastapi.responses import JSONResponse

import main

favorite_foods_router = APIRouter(tags=["favorite_foods"], prefix="/favorite_foods")


@favorite_foods_router.post("/add_favorite_foods")
def add_favorite_foods(user_id: int, food_id: int):
    try:
        main.cursor.execute("""SELECT * FROM users WHERE user_id = %s """,
                            (user_id,))

        user = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"User by {user_id} id not found"})

    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id = %s """,
                            (food_id,))

        food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})
    if food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"Food by {user_id} id not found"})

    try:
        main.cursor.execute("""INSERT INTO favorite_foods (user_id, food_id) 
                            VALUES (%s, %s)""",
                            (user_id, food_id))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": f"There was an error adding favorite food"
                                    f"ERROR: {error}"})
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Favorite food successfully added"})


@favorite_foods_router.delete("/delete_favorite_food/{favorite_food_d}")
def delete_favorite_food(favorite_food_id: int, user_id: int):
    try:
        main.cursor.execute("""SELECT * FROM favorite_foods WHERE favorite_food_id =%s AND user_id =%s""",
                            (favorite_food_id, user_id))

        favorite_food = main.cursor.fetchone()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if favorite_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"Favorite food by {favorite_food_id} id not found"})

    try:
        main.cursor.execute("""DELETE FROM favorite_foods WHERE favorite_food_id = %s AND user_id =%s""",
                            (favorite_food_id, user_id))

        main.conn.commit()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": f"An error occurred while deleting, please try again"
                                    f"ERROR: {error}"})
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Favorite food successfully deleted"})


@favorite_foods_router.get("/get_all_favorite_foods_by_user_id/{user_id}")
def get_all_favorite_foods_by_user_id(user_id: int, page: int = Query(default=1, ge=1)):
    per_page = 20

    main.cursor.execute("SELECT count(*) FROM favorite_foods")
    count = main.cursor.fetchall()[0]['count']
    if count == 0:
        return []

    max_page = (count - 1) // per_page + 1

    if page > max_page:
        page = max_page

    offset = (page - 1) * per_page

    try:
        main.cursor.execute("""SELECT * FROM favorite_foods WHERE user_id =%s LIMIT =%s OFFSET =%s""",
                            (user_id, per_page, offset))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": str(error)})

    try:
        favorite_foods = main.cursor.fetchall()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={f"An error occurred while searching for all favorite foods. ERROR {str(error)}"})

    if not favorite_foods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"User with id {user_id} has no favorite foods"})

    return {
        "favorite_foods": favorite_foods,
        "page": page,
        "total_pages": max_page,
        "total_foods": count
    }















