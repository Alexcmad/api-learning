import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    owner_id: int
    id: int
    owner: UserOut
    pass

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class Like(BaseModel):
    post_id: int
    user_id: int
    direction: conint(le=1)

class TokenData(BaseModel):
    id: Optional[str] = None
