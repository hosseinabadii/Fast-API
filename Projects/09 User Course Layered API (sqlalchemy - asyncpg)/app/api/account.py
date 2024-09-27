from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from loguru import logger
from pydantic import EmailStr

from app.crud.users import create_user, get_user_by_email
from app.db.db_setup import SessionDep
from app.db.redis_server import add_jti_to_blacklist
from app.dependencies import CurrentUserDep, GetTokenJtiDep
from app.errors import (
    InvalidCredentials,
    InvalidToken,
    PasswordsNotMatched,
    UserAlreadyRegistered,
    UserNotFound,
)
from app.mail_server import send_reset_password_email, send_verification_email
from app.oauth2 import authenticate_user, create_access_token, verify_refresh_token
from app.schemas.account import Token
from app.schemas.users import User, UserCreate
from app.utils import decode_url_safe_token

router = APIRouter(prefix="/account", tags=["Authentication"])


@router.post("/signup", response_model=User, status_code=201)
async def signup(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    session: SessionDep,
):
    db_user = await get_user_by_email(session, email)
    if db_user:
        raise UserAlreadyRegistered()
    user_data = UserCreate(email=email, password=password)
    return await create_user(session, user_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    response: Response,
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise InvalidCredentials()
    token_data = {"user_email": user.email, "token_version": user.token_version}
    access_token = await create_access_token(token_data)
    refresh_token = await create_access_token(token_data, refresh=True)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        # secure=True,
        samesite="strict",
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout(response: Response, jti: GetTokenJtiDep):
    response.delete_cookie(key="refresh_token")
    await add_jti_to_blacklist(jti)
    return {"message": "You logged out successfully"}


@router.post("/verify-account-request")
async def api_send_verification_email(current_user: CurrentUserDep):
    await send_verification_email(current_user.email)
    return {"message": "Verification email sent"}


@router.get("/verify-account", status_code=status.HTTP_202_ACCEPTED)
async def api_verify_account(token: str, session: SessionDep):
    decoded_data = decode_url_safe_token(token, salt="verification")
    if not decoded_data:
        raise InvalidToken()
    email = decoded_data.get("email")
    if not email:
        raise InvalidToken()
    db_user = await get_user_by_email(session, email)
    if not db_user:
        raise InvalidToken()
    db_user.activate()
    await session.commit()

    return {"message": "Account verified"}


@router.post("/password-reset-request")
async def api_password_reset_request(email: Annotated[EmailStr, Form()]):
    await send_reset_password_email(email)
    return {
        "message": "Please check your email for instructions to reset your password"
    }


@router.post("/password-reset-confirm", status_code=status.HTTP_202_ACCEPTED)
async def api_reset_password(
    token: str,
    new_password: Annotated[str, Form()],
    confirm_new_password: Annotated[str, Form()],
    session: SessionDep,
):
    if new_password != confirm_new_password:
        raise PasswordsNotMatched()
    decoded_data = decode_url_safe_token(token, salt="reset-password")
    if not decoded_data:
        raise InvalidToken()
    email = decoded_data.get("email")
    if not email:
        raise InvalidToken()
    db_user = await get_user_by_email(session, email)
    if not db_user:
        raise InvalidToken()
    db_user.set_hashed_password(new_password)
    db_user.update_token_version()
    await session.commit()

    return {"message": "Password reset successfully"}


@router.post("/refresh-token", response_model=Token)
async def api_refresh_token(
    jti: GetTokenJtiDep,
    request: Request,
    response: Response,
    session: SessionDep,
):
    await add_jti_to_blacklist(jti)
    refresh_token = request.cookies.get("refresh_token", "")
    refresh_token_data = await verify_refresh_token(refresh_token)
    current_user = await get_user_by_email(session, refresh_token_data.email)
    if not current_user:
        raise UserNotFound()
    if current_user.token_version != refresh_token_data.version:
        logger.warning(
            f"{current_user.email!r} attempted to use a revoked refresh token"
        )
        raise InvalidCredentials()
    token_data = {
        "user_email": refresh_token_data.email,
        "token_version": refresh_token_data.version,
    }
    await add_jti_to_blacklist(refresh_token_data.jti)
    new_access_token = await create_access_token(token_data)
    new_refresh_token = await create_access_token(token_data, refresh=True)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        # secure=True,
        samesite="strict",
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def api_me(current_user: CurrentUserDep):
    return current_user
