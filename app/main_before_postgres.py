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

my_posts = [{"title":"title post 1", "content":"content post 1", "id":1},
            {"title":"title post 2", "content":"content post 2", "id":2}]


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
    return {"Data": my_posts}




# Taking the body and converting into dictionary
# fastapi will automatically validate the Post schema
# here new_post is a pydantic model, evey pydantic model have method to convert it into dictionary
# Change the default stauts code by mentioning it in the path operation
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000)

    my_posts.append(post.dict())
    return {"data":post_dict} 

# id represent path parameter
# make sure that the data type is what is required 

@app.get("/posts/{id}")
# here the :int will perform the validation for integar and convert into int if not already
def get_post(id:int): 
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with {id} doesn't exist")
    return {"Post Details":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Post so that the request comes with a schema
@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"Data":post_dict}


