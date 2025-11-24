from pydantic import BaseModel, ConfigDict

class QuestionSubject(BaseModel):
    # id: int
    subject: str

    class Config:
        # orm_mode = True # ORM 객체를 Pydantic 객체로 변환 가능하게 설정
        model_config = ConfigDict(from_attributes=True)

