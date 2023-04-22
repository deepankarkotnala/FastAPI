from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

import uvicorn

app = FastAPI()

### For data validation - Only title and content is allowed. Both in string format. 
class Post(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data":"new post"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
