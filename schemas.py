#Create Pydantic schemas for validation and serialization.

from pydantic import BaseModel
from typing import List, Optional


#User Schemas
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class config:
        orm_mode = True
    

#Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    completed: bool
    owner_id: int

    class config:
        orm_mode = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]


