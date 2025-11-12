'''
데이터 베이스 연결 관련 설정(SQLAlchemy 엔진, 세션 관리 등)
pip install sqlalchemy
pip install alembic, alembic init alembic
alembic.ini 데이터베이스 설정 파일, sqlalchemy.url = 부분에 db url을 정의
alembic revision --autogenerate -m "create question table"
alembic upgrade head
sqlite3 MyFirstDB.db, .tables, .schema question

반복되는 쿼리를 객체 단위로 생성해서 이를 해결하고자 ORM(Object Relational Mapping) 사용
ORM: 객체와 관계형 데이터베이스의 데이터를 매핑해주는 기술
SQLAlchemy: 파이썬에서 가장 널리 사용되는 ORM 라이브러리
'''

from sqlalchemy import create_engine    # db와 연결 가능한 engine 생성
from sqlalchemy.orm import sessionmaker # ORM을 저장할 임시 메모리 공간
from sqlalchemy.orm import declarative_base # Mapping을 위한 Base 클래스 생성

engine = create_engine('sqlite:///./MyFirstDB.db', echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # 모델 클래스가 상속받아야 하는 Base 클래스 정의
