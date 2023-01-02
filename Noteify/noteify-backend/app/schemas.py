from xmlrpc.client import DateTime
from pydantic import BaseModel, EmailStr, conint
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class ImageGet(BaseModel):
    docname: str


class PostBase(BaseModel):
    subject_code: str
    curr_version: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_username: str
    published: bool

    class Config:
        orm_mode = True


class PostMod(PostBase):
    id: int
    created_at: datetime
    owner_username: str
    published: bool
    revision: list

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    curr_version: str


class PostModUpdate(BaseModel):
    revision: list
    published: bool


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class PostModOut(BaseModel):
    Post: PostMod
    votes: int

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class ModeratorCreate(BaseModel):
    username: str
    name: str
    email: EmailStr


class ModeratorLogin(BaseModel):
    username: str
    uuid_pwd: str


class ModeratorOut(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    username: str
    name: str
    email: EmailStr
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
