from sqlalchemy.orm import Session
from .. import oauth2
from .. import models, schemas
from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix="/like",
                   tags=['Likes'])


@router.post("/", status_code=201)
def like(like: schemas.Like,
         db: Session = Depends(get_db),
         user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"Post with id {like.post_id} does not exist")
    like_query = db.query(models.Likes).filter(models.Likes.post_id == like.post_id, models.Likes.user_id == user.id)
    found_like = like_query.first()
    if like.direction == 1:
        if found_like:
            raise HTTPException(status_code=409,
                                detail=f"Post {like.post_id} already liked by {user.id}")
        new_like = models.Likes(post_id=like.post_id, user_id=user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully liked post"}
    else:
        if not found_like:
            raise HTTPException(status_code=404,
                                detail=f"Post {like.post_id} not liked by user {user.id}")
        db.delete(found_like)
        db.commit()
        return {"message": "Successfully unliked post"}
