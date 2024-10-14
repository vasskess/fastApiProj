from pydantic import BaseModel, EmailStr


class MainPost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: float


class CreatePost(MainPost):
    pass


class UpdatePost(MainPost):
    pass


class PostResponse(MainPost):

    class Config:
        from_attribute = True
