from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Base fields shared across schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_complete: bool = False


# Data required when CREATING a todo
class TodoCreate(TodoBase):
    title: str
    description: Optional[str] = None
    is_complete: bool = False


# Data required when UPDATING a todo
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None


# Data returned in RESPONSES (matches DB output)
class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Required so Pydantic can convert SQLAlchemy ORM objects into JSON
    model_config = ConfigDict(from_attributes=True)