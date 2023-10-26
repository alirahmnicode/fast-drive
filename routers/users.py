from datetime import timedelta
from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException, Depends, HTTPException, status
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sql.database import SessionLocal
from sql import schemas, crud
from utility import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from pyd_models import Token


router = APIRouter()


@router.post("/token/", response_model=Token, tags=["users"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users_db = crud.get_users(db=SessionLocal())
    user = authenticate_user(users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup/", response_model=Token, tags=["users"])
def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    username = form_data.username
    hashed_password = get_password_hash(form_data.password)
    user_schema = schemas.UserCreate(username=username, hashed_password=hashed_password)
    user = crud.create_user(db=db, user=user_schema)

    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
