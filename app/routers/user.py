from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db




router = APIRouter(prefix = "/users", tags = ["Users"])





'''
---------------------------------------------------
GET (Read)
---------------------------------------------------
'''

@router.get('/{uid}', response_model=schemas.UserReponse)
async def getUser(uid: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == uid).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {uid} not found!")

    return user



'''
---------------------------------------------------
POST (Create)
---------------------------------------------------
'''

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserReponse)
async def createUser(req: schemas.UserCreate ,db: Session = Depends(get_db)):
    
    #hash the password
    hashed = utils.hash(req.password)
    req.password = hashed # set password to hashed

    new_user = models.User(**req.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

