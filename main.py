import os
import shutil
from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from sqlalchemy.orm import Session
from sql.database import SessionLocal, engine
from sql import models, schemas, crud

from utility import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    oauth2_scheme,
)
from pyd_models import UserModel, Token

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token/", response_model=Token)
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


@app.post("/signup/")
def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    username = form_data.username
    password = get_password_hash(form_data.password)
    user_schema = schemas.User(username=username, password=password)
    user = crud.create_user(db=db, user=user_schema)

    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@app.get("/foolders/", response_model=List[schemas.Foolder])
def get_foolders(
    user: Annotated[UserModel, Depends(get_current_user)], db: Session = Depends(get_db)
):
    return crud.get_foolders(db=db, user_id=user.id)


@app.post("/foolders/", response_model=schemas.Foolder)
def create_foolder(
    foolder: schemas.FoolderCreate,
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
        with open(file_path, 'wb') as f:
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
