from sqlalchemy.orm import Session
from models import Question
from domain.question.question_dto import QuestionCreateRequest

class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    # 전체 질문 목록 조회
    def get_questions(self):
        return self.db.query(Question).all()
    
    # id로 개별 질문 조회
    def get_question(self, question_id: int):
        return self.db.query(Question).filter(Question.id == question_id).first()
    
    # 새로운 질문 생성
    def create_question(self, question_data: QuestionCreateRequest):
        new_question = Question(
            subject=question_data.subject,
            content=question_data.content
        )
        self.db.add(new_question)
        self.db.commit()
        self.db.refresh(new_question)
        return new_question
