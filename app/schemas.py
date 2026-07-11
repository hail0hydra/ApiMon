from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title:  str
    content: str
    published: bool = True # default hence optional

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    # other 3 are inherited
    # would not send ID and Created_At fields.

    # by default the sql queries dont return DICT
    # they return SQLAlchemy Model.

    # Below line tells pydantic to convert it to dict or else pydantic throws ERRORS
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserReponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Auth

class UserLogin(BaseModel):
    email: EmailStr
    password: str
