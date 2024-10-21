from datetime import datetime

from pydantic import BaseModel, EmailStr


class MainPost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: float


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime


class CreatePost(MainPost):
    pass


class UpdatePost(MainPost):
    pass


class PostResponse(MainPost):

    class Config:
        from_attribute = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    phone: str


class UserResponse(CreateUser):
    email: EmailStr
    created_at: datetime = datetime.now()

    class Config:
        from_attribute = True
