from typing_extensions import Annotated
from typing import List

from fastapi import APIRouter, status
from fastapi import APIRouter, Depends
from fastapi import Depends

from pyd_models import UserModel, FoolderBase, Foolder, FoolderUpdate, FoolderFiles
from utility import get_current_user
from sql import crud, models


router = APIRouter()


@router.get("/", response_model=List[Foolder])
def get_foolders(user: Annotated[UserModel, Depends(get_current_user)]):
    orm = crud.SqlORM(models.Foolder)
    return orm.get_owner_objects(owner_id=user.id)


@router.get("/{foolder_id}/", response_model=FoolderFiles)
def get_foolder(user: Annotated[UserModel, Depends(get_current_user)], foolder_id: int):
    orm = crud.SqlORM(models.Foolder)
    obj = orm.get_owner_object_by_id(owner_id=user.id, id=foolder_id)
    return obj


@router.post("/")
def create_foolder(
    foolder: FoolderBase,
    user: Annotated[UserModel, Depends(get_current_user)],
):
    orm = crud.SqlORM(models.Foolder)
    return orm.create_object(name=foolder.name, owner_id=user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_foolder(
    foolder_id: int, user: Annotated[UserModel, Depends(get_current_user)]
):
    orm = crud.SqlORM(models.Foolder)
    orm.delete_owner_object(foolder_id, user.id)


@router.put("/", status_code=status.HTTP_200_OK)
def update_foolder(
    foolder: FoolderUpdate, user: Annotated[UserModel, Depends(get_current_user)]
):
    orm = crud.SqlORM(models.Foolder)
    orm.update_owner_object(obj_id=foolder.id, owner_id=user.id, name=foolder.name)
