import sqlite3
import time

from database import create_posts_table
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


while True:
    try:
        conn = sqlite3.connect("db.sqlite", check_same_thread=False)
        cursor = conn.cursor()
        create_posts_table(conn, cursor)
        break
    except sqlite3.Error as error:
        print("Connecting to database failed!")
        print(f"Connection Error: {error}")
        print("Waiting for 5 seconds...")
        time.sleep(5)


@app.get("/")
def index():
    content = """
    <h1>Welcome to my API</h1>
    <p>Please check the <a href="http://127.0.0.1:8000/docs">documentation</a> page.</p>
    """
    return HTMLResponse(content)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (?, ?) RETURNING * """,
        (post.title, post.content),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"post_detail": new_post}


@app.get("/posts")
def read_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.get("/posts/{post_id}")
def read_post(post_id: int):
    cursor.execute("""Select * FROM posts WHERE id = ?""", (post_id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"No post with {post_id=} found!")
    return {"post_detail": post}


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    cursor.execute(
        """Update posts SET
        title = ?, content = ? WHERE id = ?
        RETURNING *""",
        (post.title, post.content, post_id),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=404, detail=f"No post with {post_id=} found!")
    return {"updated_post_detail": updated_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = ? RETURNING *""", (post_id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=404, detail=f"No post with {post_id=} found!")
