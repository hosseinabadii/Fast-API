from typing import Annotated

from crud.users import get_user_by_email
from db.db_setup import SessionDep
from db.models.user import User as DBUser
from fastapi import Depends, HTTPException, status
from oauth2 import verify_access_token
from schemas.account import TokenData

AccessTokenDep = Annotated[TokenData, Depends(verify_access_token)]


async def get_current_user(token_data: AccessTokenDep, session: SessionDep) -> DBUser:
    current_user = await get_user_by_email(session, token_data.email)
    if not current_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
    return current_user


CurrentUserDep = Annotated[DBUser, Depends(get_current_user)]


async def get_current_active_user(current_user: CurrentUserDep) -> DBUser:
    if not current_user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Your account is not active.")
    return current_user


CurrentActiveUserDep = Annotated[DBUser, Depends(get_current_active_user)]


async def get_current_admin_user(current_user: CurrentActiveUserDep):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowd to do this action.",
        )
    return current_user


CurrentAdminUserDep = Depends(get_current_admin_user)
