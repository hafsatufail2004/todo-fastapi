from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)



postgresql_url = f"db connection string"

engine = create_engine(postgresql_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
   

app: FastAPI = FastAPI(lifespan=lifespan)


@app.post("/task/")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/task/")
def read_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).all()
        return task

@app.delete("/task/")
def delete_task(task: Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()

        session.delete(db_task)
        session.commit()
        return "Task deleted ...!"


@app.put("/task/")    
def update_task(task: Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()

        db_task.content = task.content
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        print("Updated task:", db_task)
        return db_task
    

    