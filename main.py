from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import engine, get_db
import models
from schemas import TodoCreate, TodoUpdate, TodoResponse, UserCreate, UserUpdate, UserResponse

# Create tables in PostgreSQL automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")


# =============================================================================
# HEALTH / BASE ENDPOINTS
# =============================================================================


@app.get("/")
def root():
    return {"message": "Todo API is running"}


# =============================================================================
# ORM ROUTES (SQLAlchemy)
# =============================================================================


# =============================================================================
# TODO ROUTES
# =============================================================================


# GET ALL
@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos


# GET ONE
@app.get("/todos/{id}", response_model=TodoResponse)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {id} not found",
        )
    return todo


# CREATE (POST)
@app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# UPDATE (PUT)
@app.put("/todos/{id}", response_model=TodoResponse)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    updated_todo = todo_query.first()

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {id} not found",
        )

    # Convert schema to dict, ignoring fields that weren't passed in Postman
    update_data = todo.model_dump(exclude_unset=True)

    todo_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(updated_todo)

    return updated_todo


# DELETE
@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)

    if not todo_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {id} not found",
        )

    todo_query.delete(synchronize_session=False)
    db.commit()

    # 204 No Content shouldn't return a body
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =============================================================================
# USER ROUTES
# =============================================================================

# GET ALL
@app.get("/users", response_model=List[UserResponse])
def get_users(db : Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

# GET ONE
@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return user

# CREATE (POST)
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db : Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# UPDATE (PUT)
@app.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    updated_user = user_query.first()
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    
    update_data = user.model_dump(exclude_unset=True)

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(updated_user)
    
    return updated_user

    
# DELETE
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    
    user_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# =============================================================================
# RAW SQL ROUTES (Uncomment below to test with psycopg cursor instead of ORM)
# =============================================================================

# from database import get_db_connection
# conn = get_db_connection()
# cursor = conn.cursor()

# @app.get("/sql/todos")
# def get_todos_sql():
#     cursor.execute("SELECT * FROM todos;")
#     return {"data": cursor.fetchall()}

# @app.get("/sql/todos/{id}")
# def get_todo_sql(id: int):
#     cursor.execute("SELECT * FROM todos WHERE id = %s;", (id,))
#     todo = cursor.fetchone()
#     if not todo:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
#     return {"data": todo}

# @app.post("/sql/todos", status_code=status.HTTP_201_CREATED)
# def create_todo_sql(todo: TodoCreate):
#     cursor.execute(
#         "INSERT INTO todos (title, description) VALUES (%s, %s) RETURNING *;",
#         (todo.title, todo.description)
#     )
#     new_todo = cursor.fetchone()
#     conn.commit()
#     return {"data": new_todo}

# @app.delete("/sql/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo_sql(id: int):
#     cursor.execute("DELETE FROM todos WHERE id = %s RETURNING *;", (id,))
#     deleted_todo = cursor.fetchone()
#     conn.commit()
#     if not deleted_todo:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)