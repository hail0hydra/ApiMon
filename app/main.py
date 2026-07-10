from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
# from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine, get_db



app = FastAPI() # FastAPI instance

# Post Schema
class Post(BaseModel): #extends BaseModel, inherits it, etc
    title:  str
    content: str
    published: bool = True # default


'''
Database
'''


models.Base.metadata.create_all(bind=engine)

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# if DB connection fails, HTTP Server for API is not started
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='ApiMon DB', user=DB_USER, password=DB_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        print("\t[+] Database Connection was successful")
        break
    except Exception as e:
        print("Connection to DB failed")
        print(e)
        time.sleep(2) # Bruh why not have an async function do this, and if the Async func fails, stop everything


myPosts = [
        {"title": "title of post 1", "content": "content of post 1", "published": False,  "id": 1},
        {"title": "favourite foods", "content": "I like pasta", "published": True,  "id": 2},
        {"title": "welcome to the dojo", "content": "The python Ninja welcomes you", "published": False,  "id": 0},
] # storing in memory




'''
Endpoints
'''

# GET
@app.get('/')
async def root():
    return {"message":"Welcome to my APIMon ( > - < )"} # auto convert to JSON

@app.get('/posts')
async def getPosts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get('/posts/{pid}') # PATH PARAMETER
async def getPost(pid: int): # this checks if passed data can be converted to int or not, if Yes then it converts it. No longer int() conversions
    # if not post:
    #     # res.status_code = status.HTTP_404_NOT_FOUND
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (pid,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} was not found") # simple handler with response

    return {"data": post}


# SQLALCHEMY bs
# @app.get('/sqlalchemy')
# async def testPost(db: Session = Depends(get_db)):
#
#     posts = db.query(models.Post).all()
#     return {"data": posts}



# POST
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def createPost(req: Post, db: Session = Depends(get_db)): # using the Post pydantic Model/Schema
    # because of pydantic model being used, it will auto validate the required things mentioned in the model
    # print(req)
    # print(req.model_dump()) # converts to dict, all pydantic Models have this method

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (req.title, req.content, req.published))
    # new_post = cursor.fetchone()
    #
    # conn.commit()



    ## unpacking dictionary
    # print(**req.model_dump())

    # new_post = models.Post(title=req.title, content=req.content, published=req.published)
    new_post = models.Post(**req.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *

    return {"data": new_post}


# DELETE
# @app.delete('/posts/{pid}', status_code=status.HTTP_204_NO_CONTENT)
@app.delete('/posts/{pid}') #buddy you can send a 200 back. there is no restriction as such.
async def deletePost(pid: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (pid,))
    deleted = cursor.fetchone()

    conn.commit()

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {pid} does not exist")

    return {"deleted": deleted}


# UPDATE with PUT
@app.put('/posts/{pid}')
async def updatePost(pid:int, req: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (req.title, req.content, req.published, pid))

    post = cursor.fetchone()

    conn.commit()

    if not post:

        cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (req.title, req.content, req.published))
        conn.commit()
        raise HTTPException(status_code=status.HTTP_201_CREATED,detail=f"new post created!")

    return {"updated": post}
