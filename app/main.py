from typing import List
from fastapi import FastAPI, Response, HTTPException, Depends
import models
import schemas
import utils
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


@app.post("/users", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db :Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users")
def get_user(user: schemas):
    pass
