from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # settgin default hashing algorithm


def hash(password: str):
    return pwd_context.hash(password)
