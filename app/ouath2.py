from jose import JWSError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta



# SECRET KEY
# Algorithm // HS256
# Expiration Time



load_dotenv()

# openssl rand -hex 32
SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def createAccessToken(data: dict):
    
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
