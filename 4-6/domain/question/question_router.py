from fastapi import APIRouter
from models import Question
from database import Session


router = APIRouter(prefix='/api/question')


@router.get('/')
def question_list():
    '''
    Question 테이블 전체 목록 반환 (DB 연결 해제 안함 -> 커넥션 누수)
    '''
    db = Session()
    questions = db.query(Question).all()
    
    return questions


@router.get('/leak-test')
def leak_test():
    db = Session()
    questions = db.query(Question).all()
    return {"count": len(questions)}

# 1..30 | forEach-Object {curl http://127.0.0.1:8000/api/question/leak-test}