from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import uvicorn
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True   ### providing an optional field which defaults to true 
    rating: Optional[int] = None  ### Fully optional field which defaults to None 

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='pass', 
                                cursor_factory=RealDictCursor)    
        cursor = conn.cursor()
        print("Connected to the database")
        break
    
    except Exception as e:
        print("===>Connection to the database failed\n", e)
        time.sleep(2)
    
## Instead of having a database, we will store the data in men=mory (for now)
my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1}, 
            {"title": "favourite foods", "content":"I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

### ----------------------- Routes -----------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return {"data":posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    """
    We do not directly write VALUES ((posts.title), (posts.content) , ... ) because
    this makes our code vulnerable to SQL INJECTION. 
    If we pass using %s, then this is checked for any weird sql inputs and after being sanitized, is passed to the DB.
    So we are kind of safe from SQL INJECTION now.
    """
    
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}


@app.get("/posts/{id}") ### id field is referred to as a path parameter 
def get_post(id: int, response: Response):
    
    ## A comma after str(id) is required .. otherwise we are getting a weird error. There is no explanation online.
    cursor.execute(""" SELECT * FROM posts where id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id {id} was not found")
    return({"post_detail": post})


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
### When we are sending back HTTP 204 after delete, then we should not send any data back. 
### This is the expected behavior implemented in fastapi. 


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *  """, 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"message":updated_post}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
