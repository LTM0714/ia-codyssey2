'''
FastAPI 실행 진입점(앱을 시작하는 파일, 라우터 등록)
FastAPI에서 DB세션을 의존성으로 주입받는 구조
'''

from fastapi import FastAPI
from database import engine
import models
from domain.question.question_router import router as question_router

# 모델로부터 테이블 생성(Alembic 사용 전 초기 개발용)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 단순 테스터용 라우터(서버 정상적으로 작동하는지)
@app.get('/')
def read_root():
    return {'message': 'Hello World!'}

# 라우터 등록
app.include_router(question_router)