import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class TaskBase(BaseModel):
    content: str
    completed: bool = False


class TaskAdd(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    created_at: datetime.datetime
    completed_at: datetime.datetime
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

