'''
FastAPI 실행 진입점(앱을 시작하는 파일, 라우터 등록)
'''

from fastapi import FastAPI
from database import engine
import models
from domain.question.question_router import router as question_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 모델로부터 테이블 생성(Alembic 사용 전 초기 개발용)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='화성 기지 연구 기록 시스템',
    description='연구 결과 및 재고 관리를 위한 게시판 API',
    version='1.0.0'
)

# 단순 테스터용 라우터(서버 정상적으로 작동하는지)
@app.get('/')
def read_root():
    return {'message': '화성 기지 연구 기록 시스템 API 서버가 정상 작동 중입니다.'}

# 라우터 등록
app.include_router(question_router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 정적 파일 제공 설정
app.mount("/static", StaticFiles(directory="frontend", html=True), name="frontend")

# 정적 파일 제공 (index.html)
@app.get('/index', response_class=HTMLResponse)
def get_index():
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
