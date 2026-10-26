import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import settings

security = HTTPBasic()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    user_ok = secrets.compare_digest(
        credentials.username.encode(), settings.basic_auth_user.encode()
    )
    password_ok = secrets.compare_digest(
        credentials.password.encode(), settings.basic_auth_password.encode()
    )
    if not (user_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
