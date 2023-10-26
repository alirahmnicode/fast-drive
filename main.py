import os
import shutil
from typing import List

from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import HTMLResponse
from typing_extensions import Annotated

from routers import users

from sqlalchemy.orm import Session
from sql.database import SessionLocal, engine
from sql import models, schemas, crud

from utility import get_current_user, get_db
from pyd_models import UserModel


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)


@app.get("/foolders/")
def get_foolders(
    user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)
):
    return crud.get_foolders(db=db, user_id=user.id)


@app.post("/foolders/")
def create_foolder(
    foolder,
    user: Annotated[UserModel, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.create_foolder(db=db, foolder=foolder, user_id=user.id)


@app.post("/files/")
def create_file(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    path = "files"
    for file in files:
        # Define the folder where you want to save the uploaded file
        folder_path = "sql"
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        # Save the file to the specified folder
        file_name = file.filename
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as f:
            print(file_path)
            shutil.copyfileobj(file.file, f)
            crud.create_file(db, file_name)
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
