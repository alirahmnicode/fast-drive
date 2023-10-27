from typing_extensions import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi import Depends

from pyd_models import UserModel, FoolderBase, Foolder
from utility import get_current_user
from sql import crud, models


router = APIRouter()


@router.get("/foolders/", response_model=List[Foolder])
def get_foolders(user: Annotated[UserModel, Depends(get_current_user)]):
    orm = crud.SqlORM(models.Foolder)
    return orm.get_owner_objects(owner_id=user.id)


@router.post("/foolders/")
def create_foolder(
    foolder: FoolderBase,
    user: Annotated[UserModel, Depends(get_current_user)],
):
    orm = crud.SqlORM(models.Foolder)
    return orm.create_object(name=foolder.name, owner_id=user.id)
