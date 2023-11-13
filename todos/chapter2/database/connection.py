from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABSE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

# sqlalchemy를 사용해 데이터베이스에 접근하기 위해 engine 객체를 하나 생성
engine = create_engine(DATABSE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 위에서 만든 engine 객체를 사용해 session 생성(데이터베이스와의 연결)

# DB에 접근하기 위한 생성자
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
