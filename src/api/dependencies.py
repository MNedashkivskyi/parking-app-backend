from fastapi import HTTPException, status, Request
from os import getenv

from src.api.resources.auth import validate_session_token, obtain_user_id_from_session


def authorize(request: Request):
    if getenv('MODE') != 'PROD':
        return
    if not validate_session_token(request.cookies.get("SESSION_TOKEN")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You must be logged in to access this resource!")


def obtain_user_id(request: Request):
    session_token = request.cookies.get("SESSION_TOKEN")
    user_id = obtain_user_id_from_session(session_token)
    return user_id
