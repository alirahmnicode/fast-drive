from typing import List, Union

from pydantic import BaseModel


class File(BaseModel):
    name: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True
