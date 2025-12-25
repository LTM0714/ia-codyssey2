'''
데이터 베이스 연결 관련 설정(SQLAlchemy 엔진, 세션 관리 등)
pip install sqlalchemy, alembic
alembic init alembic
alembic.ini 데이터베이스 설정 파일에서 sqlalchemy.url = {db url}, 예시: sqlite:///./MySecDB.db
alembic revision --autogenerate -m "create question table"
alembic upgrade head
sqlite3 MySecDB.db, .tables, .schema question

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

반복되는 쿼리를 객체 단위로 생성해서 이를 해결하고자 ORM(Object Relational Mapping) 사용
ORM: 객체와 관계형 데이터베이스의 데이터를 매핑해주는 기술
SQLAlchemy: 파이썬에서 가장 널리 사용되는 ORM 라이브러리
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # ORM을 저장할 임시 메모리 공간, Mapping을 위한 Base 클래스 생성
# from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = 'sqlite:///./board.db' # SQLite DB 파일 경로 지정

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
) # 1. DB 엔진 생성(DB와 실제로 연결하는 통로)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 2. 세션 생성, DB와 통신할 수 있는 객체가 만들어짐

Base = declarative_base() # 3. ORM 모델이 상속받아야 하는 Base 클래스 정의


def get_db():
    db = Session()
    print('DB connect')
    try:
        yield db
    finally:
        db.close()
        print('DB close')

'''
db_context 실행 -> db 연결 -> yield db 라우터에 전달 -> 요청 종료 -> 자동 종료 처리
'''