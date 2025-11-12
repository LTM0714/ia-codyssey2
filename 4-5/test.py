from models import Base, Question
from database import Session

session = Session()

print(session)

print(Base.metadata.tables) # 실질적으로 테이블 생성이 아닌 metadata에 등록

# question1 = Question(subject="첫 번째 질문", content="FastAPI가 뭐에요?")

# session.add(question1)

# session.commit()