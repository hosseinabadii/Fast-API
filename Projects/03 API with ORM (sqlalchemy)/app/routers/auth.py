from typing import Annotated

from db.db_setup import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from oauth2 import create_access_token
from operations.user import get_user_by_email
from schemas.token import Token
from sqlalchemy.orm import Session
from utils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = get_user_by_email(session, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    verified = verify_password(form_data.password, str(user.password))
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    access_token = create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
