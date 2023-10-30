from typing_extensions import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi import Depends

from pyd_models import UserModel, FoolderBase, Foolder, FoolderUpdate
from utility import get_current_user
from sql import crud, models


router = APIRouter()


@router.get("/", response_model=List[Foolder])
def get_foolders(user: Annotated[UserModel, Depends(get_current_user)]):
    orm = crud.SqlORM(models.Foolder)
    return orm.get_owner_objects(owner_id=user.id)


@router.post("/")
def create_foolder(
    foolder: FoolderBase,
    user: Annotated[UserModel, Depends(get_current_user)],
):
    orm = crud.SqlORM(models.Foolder)
    return orm.create_object(name=foolder.name, owner_id=user.id)


@router.delete("/")
def delete_foolder(
    foolder_id: int, user: Annotated[UserModel, Depends(get_current_user)]
):
    orm = crud.SqlORM(models.Foolder)
    orm.delete_owner_object(foolder_id, user.id)


@router.put("/")
def update_foolder(
    foolder: FoolderUpdate, user: Annotated[UserModel, Depends(get_current_user)]
):
    orm = crud.SqlORM(models.Foolder)
    orm.update_owner_object(
        obj_id=foolder.id, owner_id=user.id, name=foolder.name
    )
