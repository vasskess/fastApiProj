import psycopg2
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg2.connect(
        host="localhost", database="postgres", user="postgres", password="vaskes"
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL")
except psycopg2.Error as e:
    print("No database connection")
    print(f"Error was: {e}")


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
    cursor.execute(" SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published, post.rating),
    )  # This is the proper syntax to prevent SQLinjection !!!
    new_post = cursor.fetchone()
    conn.commit()  # This is how you safe in the DB !
    return {"post": new_post}


@app.get("/post/{id}")
def get_post(id: int):
    cursor.execute(" SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"post": post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(
        " UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
        (
            post.title,
            post.content,
            post.published,
            post.rating,
            id,
        ),
    )
    conn.commit()
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"post": updated_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(" SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    cursor.execute(" DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    return {"message": "Post successfully deleted"}
