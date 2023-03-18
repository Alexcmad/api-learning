from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_cred : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="Invalid Credentials")
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=404,
                            detail="Invalid Credentials")

    acces_token = oauth2.create_access_token(data={"id": user.id})
    return {"access_token": acces_token, "token_type": "bearer"}
