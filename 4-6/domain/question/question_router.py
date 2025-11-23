from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel  # 임시로 추가 삭제할 것

from models import Question
from database import Session as SessionLocal
from domain.question.question_schema import QuestionSubject


router = APIRouter(prefix='/api/question')

def get_db():
    db = SessionLocal()     # db 연결
    try:
        yield db            # 해당 세션을 API 함수에 전달
    finally:
        db.close()          # 사용 후 세션 종료


class QuestionCreate(BaseModel):
    subject: str
    content: str

@router.post('/')
def create_question(item: QuestionCreate, db: Session = Depends(get_db)):
    '''
    단일 Question 레코드 생성
    body 예시: {'subject': '질문 제목', 'content': '질문 내용'}
    '''
    q = Question(subject=item.subject, content=item.content)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.get('/')
def question_list(db: Session = Depends(get_db)):
    '''
    Question 테이블 전체 목록 반환
    '''
    questions = db.query(Question).all()
    return questions


@router.get('/subject', response_model=list[QuestionSubject])
def question_list2(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions


# curl -X POST 'http://127.0.0.1:8000/api/question/' -H 'Content-Type: application/json' -d "{'subject':'첫 질문','content':'내용'}"
