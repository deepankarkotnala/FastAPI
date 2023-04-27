from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts")
def create_posts(post: Post):
    # print(post.title)
    # print(post.content)
    print(post.dict())
    return {"data":post}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
