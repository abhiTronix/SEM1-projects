from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote, moderator, postmod, data
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(".env").resolve(), verbose=True)
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(post.router)
app.include_router(postmod.router)
app.include_router(user.router)
app.include_router(moderator.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(data.router)


@app.get("/")
async def root():
    return {"message": "HOLA! this is Abhishek here."}
