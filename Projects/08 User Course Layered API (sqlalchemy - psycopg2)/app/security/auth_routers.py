from typing import Annotated

from db.db_setup import SessionDep
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .auth_schemas import Token
from .constants import CREDENTIAL_EXCEPTION
from .oauth2 import authenticate_user, create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise CREDENTIAL_EXCEPTION
    access_token = create_access_token({"user_email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
