from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI() # FastAPI instance

# Post Schema
class Post(BaseModel): #extends BaseModel, inherits it, etc
    title:  str
    content: str
    published: bool = True # default
    rating: Optional[int] = None # optional integer value from Typing Library


# GET
@app.get('/')
async def root():
    return {"message":"Welcome to my APIMon ( > - < )"} # auto convert to JSON

@app.get('/posts')
async def getPosts():
    return {"data": "This is your post ⚔️⚔️⚔️ "}


# POST
@app.post('/posts')
async def createPost(req: Post): # using the Post pydantic Model/Schema
    # because of pydantic model being used, it will auto validate the required things mentioned in the model
    print(req)
    print(req.model_dump()) # converts to dict, all pydantic Models have this method
    return {"data": req}
