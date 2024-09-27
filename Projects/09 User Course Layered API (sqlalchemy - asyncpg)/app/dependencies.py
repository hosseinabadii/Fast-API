from typing import Annotated

from fastapi import Depends
from loguru import logger

from app.crud.users import get_user_by_email
from app.db.db_setup import SessionDep
from app.db.models.user import User as DBUser
from app.errors import (
    AccountNotActice,
    ForbiddenException,
    InvalidCredentials,
    UserNotFound,
)
from app.oauth2 import get_token_jti, verify_access_token
from app.schemas.account import TokenData

AccessTokenDep = Annotated[TokenData, Depends(verify_access_token)]
GetTokenJtiDep = Annotated[str, Depends(get_token_jti)]


async def get_current_user(token_data: AccessTokenDep, session: SessionDep) -> DBUser:
    current_user = await get_user_by_email(session, token_data.email)
    if not current_user:
        raise UserNotFound()
    if current_user.token_version != token_data.version:
        logger.warning(
            f"{current_user.email!r} attempted to use a revoked access token"
        )
        raise InvalidCredentials()
    return current_user


CurrentUserDep = Annotated[DBUser, Depends(get_current_user)]


async def get_current_active_user(current_user: CurrentUserDep) -> DBUser:
    if not current_user.is_active:
        raise AccountNotActice()
    return current_user


CurrentActiveUserDep = Annotated[DBUser, Depends(get_current_active_user)]


async def get_current_admin_user(current_user: CurrentActiveUserDep):
    if not current_user.is_admin:
        raise ForbiddenException()
    return current_user


CurrentAdminUserDep = Depends(get_current_admin_user)
