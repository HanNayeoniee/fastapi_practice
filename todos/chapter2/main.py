from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo
from schema.response import ListToDoResponse, ToDoSchema

app = FastAPI()

# root path에 GET 요청 보내기
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


# DB가 없으니까 데이터 미리 선언
todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션1 수강",
        "is_done": True
    },
    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션2 수강",
        "is_done": False
    },
    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션3 수강",
        "is_done": False
    }
}

# 모든 아이템 조회
@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
) -> ListToDoResponse:
    todos: List[ToDo] = get_todos(session=session)
    if order and order == "DESC":
        return ListToDoResponse(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    else:
        return ListToDoResponse(
            todos=[ToDoSchema.from_orm(todo) for todo in todos]
        )

# 아이템 1개 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
) -> ToDoSchema:
    # todo = todo_data.get(todo_id)
    todo: ToDo = get_todo(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# CreateToDoRequest을 사용하면 알아서 request body를 넣고 데이터 타입 검사까지 해줌
class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


# todo 생성
@app.post("/todos", status_code=200)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


# todo의 is_done 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True)  # CreateToDoRequest 객체 중 하나의 컬럼만 받아서 사용
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")


# todo 삭제
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")


