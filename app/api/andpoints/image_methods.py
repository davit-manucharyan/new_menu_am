import os
import shutil
import datetime
from fastapi import File, UploadFile, APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

import main


image_router = APIRouter(tags=["image"], prefix="/image")


@image_router.post("/upload_background_photo/{restaurant_id}")
def upload_background_photo(restaurant_id: int, image: UploadFile = File(...)):

    image_url = f"{os.getcwd()}/static/images/{image.filename}"

    try:
        main.cursor.execute("""SELECT restaurant_id FROM restaurants WHERE restaurant_id = %s""",
                            (restaurant_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"ERROR:": error})

    try:

        main.cursor.execute("""UPDATE restaurants SET background_image = %s WHERE restaurant_id = %s""",
                            (image_url, restaurant_id))
        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail={"ERROR": error})

    with open(image_url, "wb") as file_object:

        shutil.copyfileobj(image.file, file_object)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Background image uploaded successfully"})

