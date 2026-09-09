from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


# ======= TODO SCHEMAS =======

# Base fields shared across schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_complete: bool = False


# Data required when CREATING a todo
class TodoCreate(TodoBase):
    pass


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

# ======= USER SCHEMAS =======

class UserBase(BaseModel):
    username: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Required so Pydantic can convert SQLAlchemy ORM objects into JSON
    model_config = ConfigDict(from_attributes=True)
