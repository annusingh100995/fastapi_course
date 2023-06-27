from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import TypeVarTuple, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Default value is true
    rating: Optional[int] = None # fully optinal field, default to None 

my_posts = [{"title":"title post 1", "content":"content post 1", "id":1},
            {"title":"title post 2", "content":"content post 2", "id":2}]



while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi',user='postgres', password='annu1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database ")
        break

    except Exception as error:
        print("Failed to connect to DB")
        print("Error", error)
        time.sleep(2)


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message":"Hello World"}
  

@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * from posts""")
    posts = cursor.fetchall()
    return {"Data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    return {"Post":new_post} 


@app.get("/posts/{id}")
def get_post(id:int): 
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with {id} doesn't exist")
    return {"Post Details":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    
    updated_post = cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone() 
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    return {"Data":updated_post}


