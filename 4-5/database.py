'''
데이터 베이스 연결 관련 설정(SQLAlchemy 엔진, 세션 관리 등)
pip install sqlalchemy
pip install alembic, alembic init domain
alembic.ini 데이터베이스 설정 파일, sqlalchemy.url = 부분에 db url을 정의
alembic revision --autogenerate -m "create question table"
alembic upgrade head
sqlite3 MyFirstDB.db, .tables, .schema question

반복되는 쿼리를 객체 단위로 생성해서 이를 해결하고자 ORM(Object Relational Mapping) 사용
ORM: 객체와 관계형 데이터베이스의 데이터를 매핑해주는 기술
SQLAlchemy: 파이썬에서 가장 널리 사용되는 ORM 라이브러리
'''

from sqlalchemy import create_engine    # db와 연결 가능한 engine 생성
from sqlalchemy.ext.declarative import declarative_base # 새로운 table과 mapper 생성
from sqlalchemy.orm import sessionmaker # db와 계속 연결 상태 유지

SQLALCHEMY_DATABASE_URL = 'sqlite:///./MyFirstDB.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
