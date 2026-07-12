from fastapi import Depends, status, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, ouath2
from ..database import get_db




router = APIRouter(prefix = "/posts", tags = ['Posts'])




'''
---------------------------------------------------
GET (Read)
---------------------------------------------------
'''

@router.get('', response_model=List[schemas.PostResponse]) # since response is a List of schemas.PostResponse models
async def getPosts(db: Session = Depends(get_db), current_user = Depends(ouath2.getCurrentUser)):

    posts = db.query(models.Post).all()

    return  posts

@router.get('/{pid}', response_model=schemas.PostResponse)
async def getPost(pid: int, db: Session = Depends(get_db), current_user = Depends(ouath2.getCurrentUser)):

    post = db.query(models.Post).filter(models.Post.id == pid).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} was not found") # simple handler with response

    return post


'''
---------------------------------------------------
POST (Create)
---------------------------------------------------
'''

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def createPost(req: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(ouath2.getCurrentUser)):


    print(current_user.email)

    # new_post = models.Post(title=req.title, content=req.content, published=req.published)
    new_post = models.Post(**req.model_dump()) #unpacking dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *

    return new_post

'''
---------------------------------------------------
DELETE (Delete)
---------------------------------------------------
'''

@router.delete('/{pid}', status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(pid: int, db: Session = Depends(get_db), current_user = Depends(ouath2.getCurrentUser)):

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
async def updatePost(pid:int, req: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(ouath2.getCurrentUser)):

    post_query = db.query(models.Post).filter(models.Post.id == pid)

    post = post_query.first()

    if not post:


        # Let's just send a 404.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {pid} not found")

    post_query.update(req.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
