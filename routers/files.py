import os
import shutil
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, Path
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from sql import crud, models
from utility import get_current_user
from pyd_models import UserModel, FileModel


router = APIRouter()

FILE_PATH = "media"


def get_upload_location(username: str):
    return f"{FILE_PATH}/{username}/"


@router.get("/", response_model=List[FileModel])
def get_user_files(user: Annotated[UserModel, Depends(get_current_user)]):
    sql_orm = crud.SqlORM(models.File)
    return sql_orm.get_owner_objects(owner_id=user.id)


@router.get("/{file_id}/", response_model=FileModel)
def get_user_file(user: Annotated[UserModel, Depends(get_current_user)], file_id: int):
    sql_orm = crud.SqlORM(models.File)
    obj = sql_orm.get_owner_object_by_id(owner_id=user.id, id=file_id)
    return obj


@router.get("/dowanload/{file_id}/")
def dowanload_file(user: Annotated[UserModel, Depends(get_current_user)], file_id: int):
    sql_orm = crud.SqlORM(models.File)
    obj = sql_orm.get_owner_object_by_id(owner_id=user.id, id=file_id)
    print(obj)
    return FileResponse(
        obj.location,
        media_type=obj.content_type,
        filename=obj.name,
    )


@router.post("/")
def create_file(
    user: Annotated[UserModel, Depends(get_current_user)],
    files: List[UploadFile] = File(...),
    foolder_id: int = None
):
    sql_orm = crud.SqlORM(models.File)
    upload_location = get_upload_location(username=user.username)

    for file in files:
        file_mb_size = file.size / 1000000
        if file_mb_size < 6:
            os.makedirs(upload_location, exist_ok=True)
            file_name = file.filename
            file_path = os.path.join(upload_location, file_name)

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
                new_obj = {
                    "name": file_name,
                    "location": file_path,
                    "content_type": file.content_type,
                    "owner_id": user.id
                }

                if foolder_id:
                    new_obj.update({"foolder_id": foolder_id, "has_foolder": True})

                sql_orm.create_object(**new_obj)

    return {"filenames": [file.filename for file in files]}
