from todo.database import Base
from sqlalchemy import Column, String, Boolean, Integer


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    # created_at = ()
