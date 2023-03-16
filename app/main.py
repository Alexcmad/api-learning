import random
from typing import List
from fastapi import FastAPI, Response, HTTPException, Depends
from pydantic import BaseModel
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Now with auto reload!"}


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get({"id": id})
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    return post


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get({"id": id})
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    db.delete(post)
    db.commit()
    return Response(status_code=204)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post)
    old_post = post_query.get({"id": id})
    if not old_post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    post_query.update(post.dict())
    db.commit()
    db.refresh(old_post)
    return old_post
