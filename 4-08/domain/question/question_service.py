from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Question
from domain.question.question_dto import QuestionCreateRequest

class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    # 1. 전체 질문 목록 조회
    def get_questions(self):
        return self.db.query(Question).all()
    
    # 2. id로 개별 질문 조회
    def get_question(self, question_id: int):
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(
                status_code=404, 
                detail=f'Question with id {question_id} not found'
            )
    
    
    # 3. 새로운 질문 생성
    def create_question(self, question_data: QuestionCreateRequest):
        new_question = Question(
            subject=question_data.subject,
            content=question_data.content
        )
        self.db.add(new_question)
        self.db.commit()
        self.db.refresh(new_question)
        return new_question
    
    # 4. 질문 업데이트
    def update_question(self, question_id: int, question_data: QuestionCreateRequest):
        question = self.get_question(question_id)

        question.subject = question_data.subject
        question.content = question_data.content

        self.db.commit()
        self.db.refresh(question)
        return question
    
    # 5. 질문 삭제
    def delete_question(self, question_id: int):
        question = self.get_question(question_id)

        self.db.delete(question)
        self.db.commit()

        return question