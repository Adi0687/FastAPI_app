from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title" : "title of post 1", "content": "content of post1", "id" : 1}, 
            {"title" : "favorite foods", "content": "I like Pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_posts(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return{ "post detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    # The pop method needs the index of the element in the list
    my_posts.pop(index)
    # Raising a 204 is done because FastAPI dosent allow a message to 
    #sent when we have the 204 status code in the decorator function!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 

    # Take the data from the Post class and covert it to a dictionary
    post_dict = post.dict()
    # We add the id so that the id is in the dictionary, id is not part of the Post
    # base model class, its added while posting. So it needs to be 
    post_dict['id'] = id
    # for post with the said index, replace it with the updated post
    my_posts[index] = post_dict

    return {"data":post_dict}