from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional


class TaskBase(BaseModel):
    description: str
    completed: bool = False


class Task(TaskBase):
    created_at: datetime.datetime
    completed_at: datetime.datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class LoginUser(CreateUser):
    pass


class TokenData(BaseModel):
    id: Optional[str] = None
