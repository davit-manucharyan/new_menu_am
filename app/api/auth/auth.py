# Standard libs
import datetime


# FastAPI
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
import main
from core.confirm_registration import mail_verification_email

from core import security

from schemas.shemas import UserAdd, UserLogin


auth_router = APIRouter(tags=["auth"], prefix="/auth")


@auth_router.get("/mail_verification/{email}")
def verify_email(email: str):

    main.cursor.execute("""SELECT email FROM users WHERE email=%s""",
                        (email,))

    email_checked = main.cursor.fetchone()

    if email_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "User not found"})

    main.cursor.execute("""UPDATE users SET status=%s WHERE email=%s""",
                        (True, email))

    main.conn.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "You have successfully passed the verification"})


@auth_router.post("/add-user")
def add_user(user_data: UserAdd):
    user_password = user_data.password
    user_hashed_password = security.hash_password(user_password)

    main.cursor.execute(
        "SELECT email FROM users WHERE email = %s",
        (user_data.email,)
    )
    check_email = main.cursor.fetchone()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email is already exists"
        )

    try:
        main.cursor.execute("""INSERT INTO users (name, email, password)
                            VALUES (%s, %s, %s) RETURNING *""",
                            (user_data.name,
                             user_data.email,
                             user_hashed_password))
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error
        )

    try:
        user = main.cursor.fetchone()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error in user-add fetch!\n"
                                   f"ERR: {error}")

    if user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="User not created")

    mail_verification_email(user_data.email)

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"Message": "You have successfully registered"})


@auth_router.get("/get-one-user-by-id/{user_id}")
def get_user_by_id(user_id: int, current_user=Depends(security.get_current_user)):
    try:
        main.cursor.execute("""SELECT * FROM users WHERE user_id=%s""",
                            (user_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Error occurred while trying to select user "
                                   f"by id {user_id}\n"
                                   f"ERROR: {error}")

    try:
        user = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error occurred while trying to fetch selected user "
                                   f"by id {user_id}\n"
                                   f"ERROR: {error}")

    if user is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} was not found!")

    return user


@auth_router.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    main.cursor.execute("""delete from users where user_id=%s""",
                        (user_id,))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Successfully deleted"})


@auth_router.post("/login")
def login(login_data: UserLogin):
    user_email = login_data.email
    main.cursor.execute("""SELECT * FROM users WHERE email=%s""",
                        (user_email,))
    user = main.cursor.fetchone()

    user = dict(user)
    if not user.get("status"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": """You cannot log in because you have not 
                                        completed authentication. Please check your email."""})

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email '{user_email}' was not found!")

    user_hashed_password = user.get("password")

    if not security.verify_password(login_data.password, user_hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Wrong password")

    user_id = user.get("user_id")
    access_token = security.create_access_token({"user_id": user_id})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"Message": "Successfully logged in! Your access token",
                                 "access_token": access_token})


