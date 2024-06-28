# FastAPI
import time
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


# SQL - postgres
import psycopg2
from psycopg2.extras import RealDictCursor


from database import engine
from app.models.models import Base

# from posts import post_router
# from auth import auth_router
# from likes import like_router
# from comments import comment_router
# from settings import setting_router
# # from images import image_router
# from forgot_password import forgot_router


Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            database='post_blog',
            user='postgres',
            password='password',
            cursor_factory=RealDictCursor
            )
        print("Connection successfully")

        cursor = conn.cursor()
        break
    except Exception as error:
        print(error)
        time.sleep(3)

# cursor.execute("""SELECT * FROM possible_settings""")
#
# possible_settings = cursor.fetchone()

# if possible_settings is None:
#     cursor.execute("""INSERT INTO possible_settings (possible_languages, possible_background_colors,
#                                                                             possible_settings_font_size)
#                     VALUES (%s, %s, %s)""", (["en", "ru", "arm"], ["white", "black", "dark_blue"], 12.0))
#     conn.commit()


app = FastAPI()


@app.get("/")
def main():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})


# app.include_router(auth_router)
# app.include_router(post_router)
# app.include_router(like_router)
# app.include_router(comment_router)
# app.include_router(setting_router)
# # app.include_router(image_router)
# app.include_router(forgot_router)

