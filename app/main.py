from fastapi import FastAPI, Response, HTTPException, Depends
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Now with auto reload!"}
