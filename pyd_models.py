from pydantic import BaseModel
from typing import Union, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserModel(BaseModel):
    id: int
    username: str


class UserInDB(UserModel):
    hashed_password: str


class FoolderBase(BaseModel):
    name: str


class FoolderUpdate(FoolderBase):
    id: int


class Foolder(FoolderUpdate):
    owner_id: int

    class Config:
        orm_mode = True


class FileModel(BaseModel):
    id: int
    name: str
    location: str
    owner_id: int
    foolder_id: Optional[int] = None
    has_foolder: int

    class Config:
        orm_mode = True
