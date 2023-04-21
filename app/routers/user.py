from .. import models, schemas, utils
from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users',
                   tags=['Users'])


@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get({"id": id})
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"user with id {id} does not exist")
    return user
