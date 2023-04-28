from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import uvicorn

app = FastAPI()

'''
For data validation - Only title and content is allowed. Both in string format. 
pydantic model used for Validation 

When we create a new post, this is stored in a pydantic model. 
Pydantic model has a method called .dict which will convert the data into a dictionary. 
'''


class Post(BaseModel):
    title: str
    content: str
    published: bool = True   ### providing an optional field which defaults to true 
    rating: Optional[int] = None  ### Fully optional field which defaults to None 

## Instead of having a database, we will store the data in men=mory (for now)
my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1}, 
            {"title": "favourite foods", "content":"I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()     ## because we will get a pydantic array -- due to pydantic validation -- hence converting it to dictionary 
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/{id}") ### id field is referred to as a path parameter 
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} was not found")
    return({"post_detail": post})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
