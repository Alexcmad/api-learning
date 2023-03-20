from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from .. import models, schemas, database, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text

router = APIRouter(prefix="/tasks",
                   tags=['Tasks'])


@router.get('/', response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(database.get_db),
              user: schemas.UserOut = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == user.id).all()

    return tasks


@router.get('/{id}', response_model=schemas.TaskOut)
def get_task_by_id(id: int, db: Session = Depends(database.get_db),
                   user: schemas.UserOut = Depends(oauth2.get_current_user)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"Task with id {id} does not exist")
    if task.owner_id != user.id:
        raise HTTPException(status_code=403,
                            detail="Not authorized for this task")
    return task


@router.post('/', response_model=schemas.TaskOut)
def add_task(task: schemas.TaskAdd, db: Session = Depends(database.get_db),
             user: schemas.UserOut = Depends(oauth2.get_current_user)):
    new_task = models.Tasks(owner_id=user.id, **task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.patch('/{id}', response_model=schemas.TaskOut)
def complete_task(id: int, db: Session = Depends(database.get_db),
                  user: schemas.UserOut = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Tasks).filter(models.Tasks.id == id)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"Task with id {id} does not exist")
    if task.owner_id != user.id:
        raise HTTPException(status_code=403,
                            detail="Not authorized for this task")
    if task.completed:
        raise HTTPException(status_code=403
                            ,detail="Task is already complete")

    task_query.update({"completed": True,
                       "completed_at": text("NOW()")})
    db.commit()
    db.refresh(task)
    return task


@router.delete('/{id}')
def delete_task(id: int, db: Session = Depends(database.get_db),
                  user: schemas.UserOut = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Tasks)
    task = task_query.filter(models.Tasks.id == id).first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"Task with id {id} does not exist")
    if task.owner_id != user.id:
        raise HTTPException(status_code=403,
                            detail="Not authorized for this task")

    db.delete(task)
    db.commit()

    return Response(status_code=204)