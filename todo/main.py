from sqlalchemy import select

from fastapi import FastAPI, Response, Depends, HTTPException
from pydantic import BaseModel
import todo.models as models
from todo.database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Task(BaseModel):
    description: str
    completed: bool = False


@app.get("/")
def root():
    return {"Status": "OK"}


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return {"data": tasks}


@app.post("/tasks")
def add_task(task: Task, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"data": new_task}


@app.get("/tasks/completed")
async def get_completed_tasks(db: Session = Depends(get_db)):
    tasks = select(models.Task).filter(models.Task.completed)
    tasks = db.execute(tasks).scalars().all()

    return {"data": tasks}


@app.get("/tasks/pending")
def get_pending_tasks(db: Session = Depends(get_db)):
    tasks = select(models.Task).filter(models.Task.completed == False)
    tasks = db.execute(tasks).scalars().all()

    return {"data": tasks}


@app.get("/tasks/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get({"id": id})
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id {id} does not exist")
    return {"data": task}


@app.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get({"id": id})
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id {id} does not exist")
    db.delete(task)
    db.commit()
    return Response(status_code=204)


@app.patch("/tasks/{id}")
def complete_task(id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id, models.Task.completed == False)
    task = task_query.first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"uncompleted task with id {id} does not exist")
    task_query.update({"completed": True})
    db.commit()
    db.refresh(task)

    return {'data': task}


@app.put("/tasks/{id}")
def edit_task(task: Task, id: int, db: Session = Depends(get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == id)
    old_task = task_query.first()
    if not task:
        raise HTTPException(status_code=404,
                            detail=f"task with id{id} does not exist")
    task_query.update(task.dict())
    db.commit()
    db.refresh(old_task)

    return {'data': old_task}
