from statistics import multimode
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


def get_post_and_index(id: int):
    for index, post_entry in enumerate(my_fake_db):
        if post_entry["id"] == id:
            return post_entry, index
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found"
    )


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Hello World from my First fastAPI try"}


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
    post, index = get_post_and_index(int(id))
    return post


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    _, index = get_post_and_index(int(id))
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_fake_db[index] = post_dict
    return {"message": "Post successfully updated", "update_post": post_dict}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post, index = get_post_and_index(id)
    my_fake_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
