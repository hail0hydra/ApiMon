from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI() # FastAPI instance

# Post Schema
class Post(BaseModel): #extends BaseModel, inherits it, etc
    title:  str
    content: str
    published: bool = True # default
    rating: Optional[int] = None # optional integer value from Typing Library


myPosts = [
        {"title": "title of post 1", "content": "content of post 1", "published": False, "rating": 3, "id": 1},
        {"title": "favourite foods", "content": "I like pasta", "published": True, "rating": 4, "id": 2},
        {"title": "welcome to the dojo", "content": "The python Ninja welcomes you", "published": False, "rating": 4, "id": 0},
] # storing in memory

def findPostById(pid):
        for p in myPosts:
            if p["id"] == pid:
                return p

def deletePostById(pid):
    for p in myPosts:
        if p["id"] == pid:
            myPosts.remove(p)
            return True

# GET
@app.get('/')
async def root():
    return {"message":"Welcome to my APIMon ( > - < )"} # auto convert to JSON

@app.get('/posts')
async def getPosts():
    # return {"data": "This is your post ⚔️⚔️⚔️ "}
    return {"data": myPosts}

@app.get('/posts/{pid}') # PATH PARAMETER
async def getPost(pid: int): # this checks if passed data can be converted to int or not, if Yes then it converts it. No longer int() conversions
    print(pid)
    post = findPostById(pid)
    if not post:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {pid} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} was not found") # simple handler with response
    return {"data": post}


# POST
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def createPost(req: Post): # using the Post pydantic Model/Schema
    # because of pydantic model being used, it will auto validate the required things mentioned in the model
    # print(req)
    # print(req.model_dump()) # converts to dict, all pydantic Models have this method

    postDict = req.model_dump()
    postDict["id"] = randrange(0, 1000000)
    myPosts.append(postDict)
    print(myPosts)
    return {"data": postDict}


# DELETE
# @app.delete('/posts/{pid}', status_code=status.HTTP_204_NO_CONTENT)
@app.delete('/posts/{pid}') #buddy you can send a 200 back. there is no restriction as such.
async def deletePost(pid: int):
    deleted = deletePostById(pid)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {pid} does not exist")
    return {"message": f"post deleted successfully"}


# UPDATE with PUT
@app.put('/posts/{pid}')
async def updatePost(pid:int, req: Post):

    print(req)

    post = req.model_dump()
    post["id"] = pid

    deleted = deletePostById(pid)
    if not deleted:
        myPosts.append(post)
        raise HTTPException(status_code=status.HTTP_201_CREATED,detail=f"new post with id: {pid} created")

    myPosts.append(post)

    return {"message": "successfully updated the post"}
