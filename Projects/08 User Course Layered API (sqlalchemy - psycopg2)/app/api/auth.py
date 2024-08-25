from typing import Annotated

from crud.users import create_user, get_user_by_email
from db.db_setup import SessionDep
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas.users import User, UserCreate
from security.oauth2 import authenticate_user, create_access_token
from security.schemas import Token

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=User, status_code=201)
def signup(user: UserCreate, session: SessionDep):
    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(session, user)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise CREDENTIAL_EXCEPTION
    access_token = create_access_token(
        {"user_email": user.email, "user_is_admin": user.is_admin}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
