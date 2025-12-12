from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. SQLite DB 파일 경로 (프로젝트 폴더에 sleep.db라는 파일이 생깁니다)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sleep.db"
# 나중에 MySQL 쓸 때는 아래 주석을 풀고 위를 주석처리하면 됨
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"

# 2. 엔진 생성 (SQLite는 check_same_thread=False 옵션 필요)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 세션 생성기 (실제 DB와 대화하는 도구)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델들의 부모 클래스
Base = declarative_base()

# 5. DB 세션 의존성 함수 (API에서 가져다 쓸 것)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()