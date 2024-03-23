from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from crud import create_todo,get_todos,update_todo,delete_todo
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/")
def create_todo_api(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, todo=todo)

@app.put("/todos/")
def update_todo_api(todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    return update_todo(db=db, todo=todo)  

@app.delete("/todos/")
def delete_todo_api(todo: schemas.TodoDelete, db: Session = Depends(get_db)):
    return delete_todo(db=db, todo=todo)  


@app.get("/todos/")
def get_todo_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = get_todos(db=db, skip=skip, limit=limit)
    return todos
