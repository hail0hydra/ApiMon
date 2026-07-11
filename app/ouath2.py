from fastapi import Depends, status, HTTPException
from jose import JWSError, JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from app import schemas



# SECRET KEY
# Algorithm // HS256
# Expiration Time


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



load_dotenv()

# openssl rand -hex 32
SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def createAccessToken(data: dict):
    
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verifyAccessToken(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credential_exception

    return token_data



def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not valdate credentials", headers={'WWW-Authenticate': 'Bearer'})

    return verifyAccessToken(token, credential_exception)
