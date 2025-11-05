"""
python -m venv venv  가상환경 venv 이름으로 생성
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned (윈도우 파워쉘에서 실행 권한 설정, 현재 사용자만 허용)
venv\Scripts\activate  가상환경 활성화
deactivate  가상환경 비활성화
uvicorn todo:app --reload  FastAPI 서버 실행, uvicorn todo:app --host 0.0.0.0 --port 8000 --reload
pip install fastapi uvicorn
curl -X GET "http://127.0.0.1:8000/retrieve_todo"
curl -X POST "http://127.0.0.1:8000/add_todo" -H "Content-Type: application/json" -d "{\"task\": \"study\"}"
curl -X GET "http://127.0.0.1:8000/retrieve_todo/1"
curl -X PUT "http://127.0.0.1:8000/update_todo/1" -H "Content-Type: application/json" -d "{\"id\":1,\"task\":\"exercise\"}"
curl -X DELETE "http://127.0.0.1:8000/delete_todo/1"
"""

from fastapi import FastAPI, APIRouter, HTTPException
from model import TodoItem

# FastAPI와 라우터 인스턴스 생성
app = FastAPI()
router = APIRouter()

# todo 리스트 객체 (메모리 DB 역할)
todo_list = []

# 1. 전체 목록 조회
@router.get('/retrieve_todo')
def retrieve_todo():
    return {'todo_list': todo_list}

# 2. 항목 추가
@router.post('/add_todo')
def add_todo(todo: dict):
    if not todo or 'task' not in todo or not todo['task'].strip():
        raise HTTPException(status_code=400, detail='빈 값은 추가할 수 없습니다.')

    new_id = len(todo_list) + 1
    new_item = {'id': new_id, 'task': todo['task']}
    todo_list.append(new_item)
    return {'message': '추가 완료', 'item': new_item}

# 3. 개별 조회
@router.get('/retrieve_todo/{todo_id}')
def get_single_todo(todo_id: int):
    for item in todo_list:
        if item['id'] == todo_id:
            return {'item': item}
    raise HTTPException(status_code=404, detail='해당 ID의 항목이 없습니다.')


# 4. 수정
@router.put('/update_todo/{todo_id}')
def update_todo(todo_id: int, updated_item: TodoItem):
    for idx, item in enumerate(todo_list):  # idx는 인덱스, item은 실제 항목
        if item['id'] == todo_id:
            todo_list[idx]['task'] = updated_item.task
            return {'message': '수정 완료', 'item': todo_list[idx]}
    raise HTTPException(status_code=404, detail='수정할 항목을 찾을 수 없습니다.')
   
# 5. 삭제
@router.delete('/delete_todo/{todo_id}')
def delete_single_todo(todo_id: int):
    for item in todo_list:
        if item['id'] == todo_id:
            deleted = todo_list.pop(todo_id - 1)
            # id 재정렬
            for i, todo in enumerate(todo_list):
                todo['id'] = i + 1
            return {'message': '삭제 완료', 'id': todo_id}
    raise HTTPException(status_code=404, detail='삭제할 항목이 없습니다.')

# 라우터 등록
app.include_router(router)
