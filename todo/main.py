from . import models
from .routers import user, task, auth
from .database import engine
from fastapi import FastAPI, Response, Depends, HTTPException

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Status": "OK"}


