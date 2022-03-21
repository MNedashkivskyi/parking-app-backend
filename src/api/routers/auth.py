from fastapi import APIRouter, status, Response
from pydantic import BaseModel, Field

from src.api.resources.auth import SESSION_DURATION, perform_login, perform_register, start_session, is_admin

router = APIRouter()


class LoginRequest(BaseModel):
    username: str = Field(..., title="Username", min_length=4, max_length=64)
    password: str = Field(..., title="User password", min_length=8, max_length=64)


class RegisterRequest(BaseModel):
    username: str = Field(..., title="Username", min_length=4, max_length=64)
    password: str = Field(..., title="User password", min_length=8, max_length=64)
    mail: str = Field(..., title="User e-mail", max_length=100)


class ResetPasswordRequest(BaseModel):
    username: str = Field(..., title="Username", min_length=4, max_length=64)
    mail: str = Field(..., title="User e-mail", max_length=100)


@router.post("/login")
def login(request: LoginRequest, response: Response):
    login_result = perform_login(request.username, request.password)
    if login_result:
        response.status_code = status.HTTP_200_OK
        session_token = start_session(login_result)
        user_type = is_admin(login_result)
        response.set_cookie(key="SESSION_TOKEN", value=session_token, httponly=True, expires=SESSION_DURATION)
        return {"message": "Logged in successfully!", "id": login_result, "user_type": user_type}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Wrong username or password!"}


@router.post("/register")
def register(request: RegisterRequest, response: Response):
    register_result = perform_register(request.username, request.password, request.mail)
    if register_result:
        response.status_code = status.HTTP_200_OK
        session_token = start_session(register_result)
        response.set_cookie(key="SESSION_TOKEN", value=session_token, httponly=True, expires=SESSION_DURATION)
        return {"message": "Registered successfully!", "id": register_result}
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Could not register! Username already taken!"}


@router.post("/reset")
def reset(request: ResetPasswordRequest, response: Response):
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Not implemented yet."}
