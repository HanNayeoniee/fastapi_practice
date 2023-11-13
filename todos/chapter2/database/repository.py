from typing import List
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))

def get_todo(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))
