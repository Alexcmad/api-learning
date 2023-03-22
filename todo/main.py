from fastapi import FastAPI
from . import models
from .database import engine
from .routers import task, user, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:58333",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Status": "OK"}
