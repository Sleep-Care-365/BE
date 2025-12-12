from sqlalchemy import Column, Integer, String, Float, JSON, Date
from app.db.session import Base

class SleepReport(Base):
    __tablename__ = "sleep_reports"

    id = Column(Integer, primary_key=True, index=True) # 고유 번호 (1, 2, 3...)
    date = Column(String)       # 수면 날짜 (YYYY-MM-DD)
    sleep_score = Column(Integer) # 수면 점수
    
    # 복잡한 객체는 JSON 타입으로 저장 (SQLite, MySQL 모두 지원)
    analysis_info = Column(JSON) 
    summary = Column(JSON)
    stages = Column(JSON)       # 차트 데이터
    ai_coaching = Column(String)

    # 나중에 조회할 때 정렬하기 위해 생성일자 등도 넣을 수 있음