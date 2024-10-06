from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
@app.get("/")
async def root():
    return {"message": "Hello World from my new branch"}


@app.post("/createpost")
def create_post(post: Post):
    print(post)
    return {
        "Additional information": None, # This is null in JSON
        "Title":post.title,
        "Post": post.content,
        "Is it published": post.published,
        "Rating": post.rating
    }
