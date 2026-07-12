from fastapi import FastAPI 

from . import models
from .database import engine
from .routers import post, user, auth


app = FastAPI() # FastAPI instance



models.Base.metadata.create_all(bind=engine)


# Endpoints

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return { "message":"Welcome to my APIMon ( > - < )" }
