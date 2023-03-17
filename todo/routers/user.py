from fastapi import Depends, Response, HTTPException, APIRouter
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import utils


router = APIRouter(prefix="/users")


@router.post("/",response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
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
