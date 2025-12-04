from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.question.question_service import QuestionService

def get_question_service(db: Session = Depends(get_db)):
    '''
    QuestionService 의존성 주입 함수
    '''
    return QuestionService(db)