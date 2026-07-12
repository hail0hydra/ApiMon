from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, utils, ouath2, schemas


router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
# async def gateHouse(req: schemas.UserLogin ,db: Session = Depends(database.get_db)):
async def gateHouse(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):


    # The OAuth2PasswordRequestForm stores the user email not as email but username, the model is defined like that

    # user = db.query(models.User).filter(models.User.email == req.email).first()
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")


    # verify password

    if not utils.verify(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")

    # create a token

    access_token = ouath2.createAccessToken(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
