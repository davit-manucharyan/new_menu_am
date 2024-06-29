# FastAPI
import time
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


# SQL - postgres
import psycopg2
from psycopg2.extras import RealDictCursor


from database import engine
from app.models.models import Base


from app.api.andpoints.restaurant import restaurant_router
from app.api.auth.auth import auth_router
from app.api.auth.forgot_password import forgot_router


Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            database='new_menu_am',
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


app = FastAPI()


@app.get("/")
def main():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "OK"})


app.include_router(restaurant_router)
app.include_router(auth_router)
app.include_router(forgot_router)
