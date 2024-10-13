import psycopg2

from fastapi import FastAPI, HTTPException, status, Depends

from sqlalchemy.orm import Session

from app import models, schemas
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


@app.get("/")
async def root():
    return {"message": "Hello World from my First fastAPI try"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(" SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published, post.rating),
    # )  # This is the proper syntax to prevent SQLinjection !!!
    # new_post = cursor.fetchone()
    # conn.commit()  # This is how you safe in the DB !
    # new_post = models.Posts(
    #     title=post.title,
    #     content=post.content,
    #     published=post.published,
    #     rating=post.rating,
    # )
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"post": new_post}


@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(" SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"post": post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    # cursor.execute(
    #     " UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         post.rating,
    #         id,
    #     ),
    # )
    # conn.commit()
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    post_query.update(post.model_dump())
    db.commit()
    db.refresh(updated_post)
    return {"post": updated_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(" SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    # cursor.execute(" DELETE FROM posts WHERE id = %s", (id,))
    # conn.commit()
    db.delete(post)
    db.commit()
    return
