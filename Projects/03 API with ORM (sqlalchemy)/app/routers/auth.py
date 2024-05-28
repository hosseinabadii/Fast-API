from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .. import crud, utils, oauth2, schemas
from ..database import get_db


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    verified = utils.verify_password(form_data.password, user.password)
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    access_token = oauth2.create_access_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
