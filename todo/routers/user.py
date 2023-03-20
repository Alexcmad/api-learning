from fastapi import APIRouter, Depends, Response
from .. import schemas, models, database, utils
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users",
                   tags=['Users'])


@router.post('/', response_model=schemas.UserOut, status_code=201)
def add_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
