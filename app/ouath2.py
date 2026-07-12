from fastapi import Depends, status, HTTPException
from jose import  JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models



# SECRET KEY
# Algorithm // HS256
# Expiration Time


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



load_dotenv()

# openssl rand -hex 32
SECRET_KEY: str = os.getenv("JWT_SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def createAccessToken(data: dict):
    
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verifyAccessToken(token: str, credential_exception):

    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data



def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not valdate credentials", headers={'WWW-Authenticate': 'Bearer'})

    token_id = verifyAccessToken(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token_id.id).first()

    return user
