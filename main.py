from fastapi import FastAPI, status, HTTPException
from schemas import TodoCreate, TodoUpdate
from random import randrange


app = FastAPI()


my_posts = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Build a Todo API",
        "is_completed": False
    },
    {
        "id": 2,
        "title": "Study Python",
        "description": "",
        "is_completed": False
    }
]


# HOME
@app.get("/")
def root():
    return {"message": "Todo API is running"}


# POST
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    post_dict = todo.model_dump()
    post_dict["id"] = randrange(1, 99)

    my_posts.append(post_dict)

    return {"data": post_dict}


# GET ALL
@app.get("/todos")
def get_todos():
    return {"data": my_posts}


# GET ONE
@app.get("/todos/{id}")
def get_todo(id: int):
    for todo in my_posts:
        if todo["id"] == id:
            return {"data": todo}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with id {id} not found"
    )


# PUT
@app.put("/todos/{id}")
def update_todo(id: int, todo: TodoUpdate):
    for i, existing_todo in enumerate(my_posts):
        if existing_todo["id"] == id:

            updated_todo = todo.model_dump()
            updated_todo["id"] = id

            my_posts[i] = updated_todo

            return {"data": updated_todo}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with id {id} not found"
    )


# DELETE
@app.delete("/todos/{id}")
def delete_todo(id: int):
    for i, todo in enumerate(my_posts):
        if todo["id"] == id:
            my_posts.pop(i)

            return {
                "message": f"Successfully deleted todo number {id}"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with id {id} not found"
    )