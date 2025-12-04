"""
pyothon -m venv venv  가상환경 venv 이름으로 생성
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned (윈도우 파워쉘에서 실행 권한 설정, 현재 사용자만 허용)
venv\Scripts\activate  가상환경 활성화
deactivate  가상환경 비활성화
uvicorn todo:app --reload  FastAPI 서버 실행
pip install fastapi uvicorn
curl -X POST "http://127.0.0.1:8000/add_todo" -H "Content-Type: application/json" -d "{\"task\": \"study\"}"
curl -X GET "http://127.0.0.1:8000/retrieve_todo"
"""

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from typing import Dict, List

# FastAPI와 라우터 인스턴스 생성
app = FastAPI()
router = APIRouter()

# 1. todo 리스트 객체 (메모리 DB 역할)
todo_list: List[Dict] = []

# 2. todo_list에 새로운 항목을 추가하는 함수
@router.post('/add_todo', response_model=Dict)
def add_todo(item: Dict) -> Dict:
    if not item or all(not v for v in item.values()):
        return JSONResponse(content={'warning': '입력된 값이 없습니다!'}, status_code=400)

    todo_list.append(item)

    return {'message': '추가 완료', 'current_count': str(len(todo_list))}


# todo_list의 모든 항목을 반환하는 함수
@router.get('/retrieve_todo', response_model=Dict)
def retrieve_todo() -> Dict:

    return {'todo_list': todo_list}


# 라우터 등록
app.include_router(router)
