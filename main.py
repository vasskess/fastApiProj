from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


my_fake_db = [
    {
        "id": 1,
        "title": "Lord of the Rings",
        "content": "Book I",
        "published": True,
        "rating": 9.9,
    },
    {
        "id": 2,
        "title": "Lord of the Rings",
        "content": "Book II",
        "published": True,
        "rating": 8.5,
    },
]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Hello World from my new branch"}


@app.get("/posts")
def get_posts():
    return my_fake_db


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = len(my_fake_db) + 1
    my_fake_db.append(post_dict)
    return post
    # return {
    #     "Additional information": None, # This is null in JSON
    #     "Title":post.title,
    #     "Post": post.content,
    #     "Is it published": post.published,
    #     "Rating": post.rating
    # }
