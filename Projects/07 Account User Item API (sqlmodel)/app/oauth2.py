from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from .config import settings
from .db import get_session
from .models import TokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
FORGET_PWD_SECRET_KEY = settings.forgot_pwd_secret_key


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(
    token: Annotated[str, Depends(oauth2_scheme)], credentials_exception
):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except jwt.ExpiredSignatureError as exc:
        raise credentials_exception from exc
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

    return token_data


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    current_user = session.get(User, token_data.id)
    if not current_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return current_user


def create_reset_password_token(email: str):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}
    token = jwt.encode(data, FORGET_PWD_SECRET_KEY, ALGORITHM)
    return token


def decode_reset_password_token(token: str):
    try:
        decoded_token = jwt.decode(token, FORGET_PWD_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
