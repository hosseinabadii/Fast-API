from typing import Annotated

from crud.users import create_user, get_user_by_email
from db.db_setup import SessionDep
from dependencies import CurrentUserDep
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from oauth2 import authenticate_user, create_access_token, verify_refresh_token
from pydantic import EmailStr
from schemas.account import Token, TokenRefresh
from schemas.users import User, UserCreate
from send_email import send_reset_password_email, send_verification_email
from utils import decode_url_safe_token

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter(prefix="/account", tags=["Authentication"])


@router.post("/signup", response_model=User, status_code=201)
async def signup(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    session: SessionDep,
):
    db_user = await get_user_by_email(session, email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    user_data = UserCreate(email=email, password=password)
    return await create_user(session, user_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise CREDENTIAL_EXCEPTION
    access_token = await create_access_token({"user_email": user.email})
    refresh_token = await create_access_token({"user_email": user.email}, refresh=True)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.post("/verify-account-request")
async def api_send_verification_email(current_user: CurrentUserDep):
    await send_verification_email(current_user.email)
    return {"message": "Verification email sent"}


@router.get("/verify-account", status_code=status.HTTP_202_ACCEPTED)
async def api_verify_account(token: str, session: SessionDep):
    decoded_data = decode_url_safe_token(token, salt="verification")
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    email = decoded_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    db_user = await get_user_by_email(session, email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid token")
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
        raise HTTPException(status_code=400, detail="Passwords do not match")
    decoded_data = decode_url_safe_token(token, salt="reset-password")
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    email = decoded_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    db_user = await get_user_by_email(session, email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid token")
    db_user.set_hashed_password(new_password)
    await session.commit()

    return {"message": "Password reset successfully"}


@router.post("/refresh-token", response_model=Token)
async def api_refresh_token(refresh_token: TokenRefresh):
    payload = await verify_refresh_token(refresh_token.token)
    new_access_token = await create_access_token({"user_email": payload.email})
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
async def api_me(current_user: CurrentUserDep):
    return current_user
