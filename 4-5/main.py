'''
FastAPI 실행 진입점(앱을 시작하는 파일, 라우터 등록)
FastAPI에서 DB세션을 의존성으로 주입받는 구조
'''

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 모델로부터 테이블 생성(Alembic 사용 전 초기 개발용)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_root():
    return {'message': 'Hello World!'}