from sqlalchemy import select
from fastapi import Depends, Response, HTTPException, APIRouter
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from .. import models

router = APIRouter(prefix="/tasks")


@router.get("/",response_model=schemas.Task)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


@router.post("/",response_model=schemas.Task)
def add_task(task: schemas.TaskBase, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/completed",response_model=schemas.Task)
async def get_completed_tasks(db: Session = Depends(get_db)):
    tasks = select(models.Task).filter(models.Task.completed)
    tasks = db.execute(tasks).scalars().all()

    return tasks


@router.get("/pending",response_model=schemas.Task)
def get_pending_tasks(db: Session = Depends(get_db)):
    tasks = select(models.Task).filter(models.Task.completed == False)
    tasks = db.execute(tasks).scalars().all()

    return tasks


@router.get("/{id}",response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get({"id": id})
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id {id} does not exist")
    return task


@router.delete("/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get({"id": id})
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id {id} does not exist")
    db.delete(task)
    db.commit()
    return Response(status_code=204)


@router.patch("/{id}",response_model=schemas.Task)
def complete_task(id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id, models.Task.completed == False)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"uncompleted task with id {id} does not exist")
    task_query.update({"completed": True,
                       "completed_at": text("NOW()")})
    db.commit()
    db.refresh(task)

    return task


@router.put("/{id}",response_model=schemas.Task)
def edit_task(task: schemas.TaskBase, id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    old_task = task_query.first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id{id} does not exist")
    task_query.update(task.dict())
    db.commit()
    db.refresh(old_task)

    return old_task
