from pydantic import BaseModel  # 데이터 유효성 검사

class TodoItem(BaseModel):
    task: str   # 'task'라는 키가 필수로 있어야 하며, 값은 문자열이어야 함
