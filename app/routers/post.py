from fastapi import Depends, status, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db




router = APIRouter(
        prefix= "/posts",
        tags = ['Posts']
    )




'''
---------------------------------------------------
GET (Read)
---------------------------------------------------
'''

@router.get('/', response_model=List[schemas.PostResponse]) # to say a List of the Model is same kind
async def getPosts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return  posts

@router.get('/{pid}', response_model=schemas.PostResponse) # PATH PARAMETER
async def getPost(pid: int, db: Session = Depends(get_db)): # this checks if passed data can be converted to int or not, if Yes then it converts it. No longer int() conversions
    # if not post:
    #     # res.status_code = status.HTTP_404_NOT_FOUND
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (pid,))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} was not found") # simple handler with response
    post = db.query(models.Post).filter(models.Post.id == pid).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} was not found") # simple handler with response

    return post


'''
---------------------------------------------------
POST (Create)
---------------------------------------------------
'''

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def createPost(req: schemas.PostCreate, db: Session = Depends(get_db)): # using the Post pydantic Model/Schema
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

    return new_post

'''
---------------------------------------------------
DELETE (Delete)
---------------------------------------------------
'''

# @router.delete('/posts/{pid}', status_code=status.HTTP_204_NO_CONTENT)
@router.delete('/{pid}', status_code=status.HTTP_204_NO_CONTENT) #buddy you can send a 200 back. there is no restriction as such.
async def deletePost(pid: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (pid,))
    # deleted = cursor.fetchone()
    #
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == pid)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {pid} does not exist")

    post.delete(synchronize_session=False)
    db.commit()


'''
---------------------------------------------------
PUT (Update)
---------------------------------------------------
'''
@router.put('/{pid}', response_model=schemas.PostResponse)
async def updatePost(pid:int, req: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (req.title, req.content, req.published, pid))
    #
    # post = cursor.fetchone()
    #
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == pid)

    post = post_query.first()

    if not post:

        # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (req.title, req.content, req.published))
        # conn.commit()
        # raise HTTPException(status_code=status.HTTP_201_CREATED,detail=f"new post created!")

        # Let's just send a 404.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} not found")

    post_query.update(req.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
