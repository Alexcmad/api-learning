from .database import Base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql.expression import text


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("NOW()"))
    completed_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("NOW()"))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text("NOW()"))

