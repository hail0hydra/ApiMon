from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # settgin default hashing algorithm


def hash(password: str):
    return pwd_context.hash(password)


def verify(password, hash):
    return pwd_context.verify(password, hash)
