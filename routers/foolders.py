from typing_extensions import Annotated

from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi import Depends

from pyd_models import UserModel
from utility import get_current_user, get_db
from sql import crud
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/foolders/")
def get_foolders(
    user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)
):
    return crud.get_foolders(db=db, user_id=user.id)


@router.post("/foolders/")
def create_foolder(
    foolder,
    user: Annotated[UserModel, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.create_foolder(db=db, foolder=foolder, user_id=user.id)
