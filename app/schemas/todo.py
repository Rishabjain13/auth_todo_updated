from pydantic import BaseModel
from typing import Literal

class TodoCreate(BaseModel):
    title: str
    priority: Literal["High", "Medium", "Low"]

class TodoUpdate(BaseModel):
    title: str
    priority: Literal["High", "Medium", "Low"]
    completed: bool

class TodoResponse(BaseModel):
    id: int
    title: str
    priority: str
    completed: bool

    model_config = {"from_attributes": True}
