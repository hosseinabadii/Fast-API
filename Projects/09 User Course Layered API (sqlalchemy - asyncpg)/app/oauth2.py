from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.users import get_user_by_email
from app.db.models.user import User as DBUser
from app.db.redis_server import jti_in_blacklist
from app.errors import InvalidCredentials
from app.schemas.account import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")
Oauth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> DBUser | None:
    db_user = await get_user_by_email(session, email)
    if not db_user:
        return
    if not db_user.verify_password(password):
        return
    return db_user


async def create_access_token(
    data: dict, expires_delta: timedelta | None = None, refresh: bool = False
) -> str:
    to_encode = data.copy()
    if not expires_delta:
        if refresh:
            expires_delta = timedelta(days=settings.jwt_refresh_token_expire)
        else:
            expires_delta = timedelta(minutes=settings.jwt_access_token_expire)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"jti": str(uuid4()), "exp": expire, "refresh": refresh})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return encoded_jwt


async def get_token_jti(token: Oauth2SchemeDep) -> str:
    try:
        payload: dict = jwt.decode(
            token, settings.jwt_secret_key, [settings.jwt_algorithm]
        )
        return payload.get("jti", "")
    except Exception:
        return ""


async def verify_access_token(token: Oauth2SchemeDep) -> TokenData:
    try:
        payload: dict = jwt.decode(
            token, settings.jwt_secret_key, [settings.jwt_algorithm]
        )
        if payload.get("refresh"):
            logger.warning("Attempted to use refresh token as access token")
            raise InvalidCredentials()
        jti = payload.get("jti", "")
        if await jti_in_blacklist(jti):
            logger.warning("Attempted to use a revoked access token")
            raise InvalidCredentials()
        user_email = payload.get("user_email")
        if user_email is None:
            raise InvalidCredentials()
        token_version = int(payload.get("token_version", -1))
        return TokenData(jti=jti, email=user_email, version=token_version)
    except jwt.InvalidTokenError as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
    except Exception as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc


async def verify_refresh_token(token: str) -> TokenData:
    try:
        payload: dict = jwt.decode(
            token, settings.jwt_secret_key, [settings.jwt_algorithm]
        )
        if not payload.get("refresh"):
            logger.warning("Attempted to use access token as refresh token")
            raise InvalidCredentials()
        jti = payload.get("jti", "")
        if await jti_in_blacklist(jti):
            logger.warning("Attempted to use a revoked refresh token")
            raise InvalidCredentials()
        user_email = payload.get("user_email")
        if user_email is None:
            raise InvalidCredentials()
        token_version = int(payload.get("token_version", -1))
        return TokenData(jti=jti, email=user_email, version=token_version)
    except jwt.InvalidTokenError as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
    except Exception as exc:
        logger.error(exc)
        raise InvalidCredentials() from exc
