from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import create_todo
from crud import delete_todo
from crud import get_todo
from crud import get_todos
from crud import update_todo
from database import Base
from database import engine
from database import get_db
from schemas import TodoCreate
from schemas import TodoResponse
from schemas import TodoUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")


@app.get("/")
def home():
    return {"message": "Todo API Running"}


@app.post("/todos", response_model=TodoResponse)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db, todo)


@app.get("/todos", response_model=list[TodoResponse])
def read_all(db: Session = Depends(get_db)):
    return get_todos(db)


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update(todo_id: int, item: TodoUpdate, db: Session = Depends(get_db)):
    todo = update_todo(db, todo_id, item)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    ok = delete_todo(db, todo_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted"}