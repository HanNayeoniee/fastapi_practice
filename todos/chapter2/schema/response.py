from typing import List
from pydantic import BaseModel

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    # orm 객체를 pydantic 객체로 변환할 수 있도록 설정
    class Config:
        orm_mode = True

# pydantic BaseModel을 활용해 HTTP response 형식 지정
class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]
