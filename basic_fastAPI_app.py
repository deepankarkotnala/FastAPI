from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

import uvicorn

app = FastAPI()

### For data validation - Only title and content is allowed. Both in string format. 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True   ### providing an optional field which defaults to true 
    rating: Optional[int] = None  ### Fully optional field which defaults to None 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title)
    print(new_post.content)
    print(new_post.published)
    print(new_post.rating)
    return {"data":"new post"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
