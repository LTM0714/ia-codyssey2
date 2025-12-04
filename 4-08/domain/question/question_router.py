from fastapi import APIRouter, Depends, status

from domain.question.question_dto import (
    QuestionCreateRequest,
    QuestionViewResponse
)
from domain.question.question_service import QuestionService
from domain.question.dependencies import get_question_service

router = APIRouter(prefix='/api/question')

# 1. 전체 질문 목록 조회
@router.get('/', response_model=list[QuestionViewResponse])
def question_list(
    service: QuestionService = Depends(get_question_service)
):
    return service.get_questions()

# 2. 개별 질문 조회
@router.get('/{question_id}', response_model=QuestionViewResponse)
def get_single_question(
        question_id: int,
        service: QuestionService = Depends(get_question_service)
):
    return service.get_question(question_id)

# 3. 새로운 질문 생성
@router.post(
        '/',
        response_model=QuestionViewResponse,
        status_code=status.HTTP_201_CREATED
)
def create_question(
    question_dto: QuestionCreateRequest,
    service: QuestionService = Depends(get_question_service)
):
    return service.create_question(question_dto)

# 4. 질문 업데이트
@router.put(
    '/{question_id}',
    response_model=QuestionViewResponse,
    status_code=status.HTTP_200_OK
)
def update_question(
    question_id: int,
    question_dto: QuestionCreateRequest,
    service: QuestionService = Depends(get_question_service)
):
    return service.update_question(question_id, question_dto)

# 5. 질문 삭제
@router.delete(
    '/{question_id}',
    status_code=status.HTTP_200_OK
)
def delete_question(
    question_id: int,
    service: QuestionService = Depends(get_question_service)
):
    return service.delete_question(question_id)