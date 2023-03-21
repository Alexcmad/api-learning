from .. import models, schemas
from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import oauth2

router = APIRouter(prefix="/posts",
                   tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db),
                    limit: int= 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    return posts


@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_dict = post.dict()
    new_post = models.Post(owner_id=current_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get({"id": id})
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    return post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).get({"id": id})
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Not Authorized to Delete this Post")
    db.delete(post)
    db.commit()
    return Response(status_code=204)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post)
    old_post = post_query.get({"id": id})
    if not old_post:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Not Authorized to Delete this Post")
    post_query.update(post.dict())
    db.commit()
    db.refresh(old_post)
    return old_post
