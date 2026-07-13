from sqlalchemy.orm import Session

from models import Todo
from schemas import TodoCreate
from schemas import TodoUpdate


def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(title=todo.title)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def get_todos(db: Session):
    return db.query(Todo).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    if todo.title is not None:
        db_todo.title = todo.title

    if todo.completed is not None:
        db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return False

    db.delete(db_todo)
    db.commit()

    return True