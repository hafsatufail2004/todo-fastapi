from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    text: str

class TodoUpdate(BaseModel):
    id: int
    text: str

class TodoDelete(BaseModel):
    id: int

