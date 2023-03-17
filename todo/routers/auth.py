from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils
from fastapi import Depends, APIRouter, Response, HTTPException

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_cred : schemas.CreateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="Invalid Credentials")
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=404,
                            detail="Invalid Credentials")
    return {"token": "Example Token"}