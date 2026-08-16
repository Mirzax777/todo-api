from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str = ""


class TodoUpdate(BaseModel):
    title: str
    description: str
    is_completed: bool