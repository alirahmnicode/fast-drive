from pydantic import BaseModel
from typing import Union


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
