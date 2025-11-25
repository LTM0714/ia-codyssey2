'''
ORM 모델 정의
이것을 실행시켜 실제 db에 데이터를 생성하기 위해선 Alembic 데이터베이스 마이그레이션 도구 사용
'''

from sqlalchemy import Column, Integer, String, DateTime
from database import Base   # 가져온 Base를 상속받아 모델 매핑
from datetime import datetime

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.now)