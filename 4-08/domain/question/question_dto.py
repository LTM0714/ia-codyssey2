from pydantic import BaseModel, ConfigDict
from datetime import datetime


class QuestionCreateRequest(BaseModel):
    subject: str
    content: str


class QuestionViewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    content: str
    create_date: datetime

    # class Config:
    #     orm_mode = True

'''
orm_mode = True 설정을 통해 Pydantic 모델이 ORM 객체를 딕셔너리가 아닌 클래스 인스턴스로 인식하고, attribute 접근을 통해 데이터를 읽어 모델 생성
orm_mode = False 일 경우 딕셔너리 형태의 데이터만 처리 가능
'''