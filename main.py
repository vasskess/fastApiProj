from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
@app.get("/")
async def root():
    return {"message": "Hello World from my new branch"}


@app.post("/createpost")
def create_post(post: Post):
    print(post)
    return {f"{post.title}": f"{post.content}"}
