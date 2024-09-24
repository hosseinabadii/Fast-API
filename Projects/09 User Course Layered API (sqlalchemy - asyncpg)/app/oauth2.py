from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from config import settings
from crud.users import get_user_by_email
from db.models.user import User as DBUser
from errors import InvalidCredentials, TokenExpired
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from schemas.account import TokenData
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> DBUser | None:
    db_user = await get_user_by_email(session, email)
    if not db_user or db_user.verify_password(password):
        return
    return db_user


async def create_access_token(
    data: dict, expires_delta: timedelta | None = None, refresh: bool = False
) -> str:
    to_encode = data.copy()
    if not expires_delta:
        if refresh:
            expires_delta = timedelta(days=settings.refresh_token_expire_days)
        else:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "refresh": refresh})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


async def verify_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    try:
        payload: dict = jwt.decode(token, settings.secret_key, [settings.algorithm])
        if payload.get("refresh"):
            logger.warning("Attempted to use refresh token as access token")
            raise InvalidCredentials()
        user_email = payload.get("user_email")
        if user_email is None:
            raise InvalidCredentials()
        return TokenData(email=user_email)
    except jwt.ExpiredSignatureError as exc:
        logger.error(exc)
        raise TokenExpired() from exc
    except jwt.PyJWTError as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
    except Exception as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc


async def verify_refresh_token(token: str) -> TokenData:
    try:
        payload: dict = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if not payload.get("refresh"):
            logger.warning("Attempted to use access token as refresh token")
            raise InvalidCredentials()
        user_email = payload.get("user_email")
        if user_email is None:
            raise InvalidCredentials()
        return TokenData(email=user_email)
    except jwt.ExpiredSignatureError as exc:
        logger.error(exc)
        raise TokenExpired() from exc
    except jwt.PyJWTError as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
    except Exception as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
