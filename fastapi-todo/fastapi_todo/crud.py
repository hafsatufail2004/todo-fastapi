from sqlalchemy.orm import Session

import models
import  schemas

def get_todo(db: Session, id: int):
    return db.query(models.Todo).filter(models.Todo.id == id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
   return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(text = todo.text)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return 'Todo has been created...!'

def update_todo(db: Session, todo: schemas.TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo.id).first()
    db_todo.text = todo.text
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return 'Todo has been updated...!' 

def delete_todo(db: Session, todo: schemas.TodoDelete):
   db_todo = db.query(models.Todo).filter(models.Todo.id == todo.id).first()
   db.delete(db_todo)
   db.commit()
   return "Todo has been deleted...!"

