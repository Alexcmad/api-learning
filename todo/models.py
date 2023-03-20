from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql.expression import text

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, nullable=False, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="cascade"), nullable=False)

