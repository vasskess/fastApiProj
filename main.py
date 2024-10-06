from typing import Optional

from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from starlette import status

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


def find_post(id):
    for post_entry in my_fake_db:
        if post_entry["id"] == id:
            return post_entry
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} is not found"
    )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"Post with id: {id} is not found"}


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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = len(my_fake_db) + 1
    my_fake_db.append(post_dict)
    return post_dict


@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(int(id))
    return post
