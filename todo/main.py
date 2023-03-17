from . import models
from .routers import user, task
from .database import engine
from fastapi import FastAPI, Response, Depends, HTTPException

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(task.router)

@app.get("/")
def root():
    return {"Status": "OK"}


