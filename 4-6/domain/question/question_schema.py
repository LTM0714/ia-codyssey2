from pydantic import BaseModel
from datetime import datetime

class QuestionSubject(BaseModel):
    # id: int
    subject: str

    class Config:
        orm_mode = True
