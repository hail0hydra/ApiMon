from fastapi import Depends, FastAPI, Response, status, HTTPException

from sqlalchemy.orm import Session, query
from . import models, schemas, utils
from .database import SessionLocal, engine, get_db

from .routers import post, user




app = FastAPI() # FastAPI instance



models.Base.metadata.create_all(bind=engine)





'''
Endpoints
'''

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
async def root():
    return {
            "message":"Welcome to my APIMon ( > - < )"
            } # auto convert to JSON
