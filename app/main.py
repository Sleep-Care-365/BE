from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import analysis

#  DB 모델과 엔진 가져오기
from app.db.session import engine, Base
from app.models import report # 모델 파일 인식

# 서버 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sleep Care 365 API",
    description="졸업작품 수면 분석 AI 서비스 백엔드",
    version="1.0.0"
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 2. 라우터 등록 (prefix는 주소 앞에 붙는 말)
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])

@app.get("/")
def read_root():
    return {"message": "Hello, Sleep Care 365 Backend is running! 🌙"}

@app.get("/ping")
def ping():
    return {"status": "ok"}