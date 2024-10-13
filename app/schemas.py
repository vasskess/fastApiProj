from pydantic import BaseModel


class MainPost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: float


class CreatePost(MainPost):
    pass


class UpdatePost(MainPost):
    pass
