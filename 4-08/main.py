'''
FastAPI 실행 진입점(앱을 시작하는 파일, 라우터 등록)
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from domain.question.question_router import router as question_router

# 모델로부터 테이블 생성(Alembic 사용 전 초기 개발용)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='화성 기지 연구 기록 시스템',
    description='연구 결과 및 재고 관리를 위한 게시판 API',
    version='1.0.0'
)

# CORS 설정 (index.html이 fetch할 때 꼭 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 개발환경에서는 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],       # OPTIONS 포함 모든 메서드 허용
    allow_headers=["*"],       # 모든 헤더 허용
)

# 단순 테스터용 라우터(서버 정상적으로 작동하는지)
@app.get('/')
def read_root():
    return {'message': '화성 기지 연구 기록 시스템 API 서버가 정상 작동 중입니다.'}

# 라우터 등록
app.include_router(question_router)