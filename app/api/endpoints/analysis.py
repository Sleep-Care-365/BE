import shutil
import os
import random
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.schemas.report import SleepReportResponse
from app.services.ai_inference import ai_service
from app.db.session import get_db
from app.models.report import SleepReport

router = APIRouter()

# 업로드된 파일을 저장할 임시 폴더
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=SleepReportResponse)
async def analyze_sleep_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    # 1. 파일 임시 저장
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(f"파일 저장 완료: {file_path}")

    # 2. AI 예측 및 수면 사이클(Mock) 생성 로직
    # 실제 모델이 연결되면: predicted_stages = ai_service.predict(file_path)
    
    formatted_stages = []
    
    # 수면 단계 매핑 (0:W, 1:N1, 2:N2, 3:N3, 4:N4, 5:R)
    stage_map = {0: "W", 1: "N1", 2: "N2", 3: "N3", 4: "N4", 5: "R"}
    # 그래프 높이 (W가 제일 높고 N4가 제일 낮음)
    level_map = {0: 5, 1: 3, 2: 2, 3: 1, 4: 0, 5: 4}

    # 사람의 수면 사이클 (Wake -> N1 -> N2 -> N3 -> N4 -> N3 -> REM 반복)
    sleep_cycles = [
        # [단계코드, (최소분, 최대분)]
        (0, (10, 20)), # 입면 (Wake)
        (1, (5, 10)),  # N1
        (2, (10, 30)), # N2
        (3, (20, 40)), # N3 (깊은 잠)
        (4, (10, 20)), # N4 (매우 깊은 잠)
        (3, (10, 20)), # 다시 얕아짐
        (2, (10, 20)), 
        (5, (10, 20)), # 첫 REM
        (2, (20, 40)), # 2번째 사이클
        (3, (20, 30)), 
        (5, (20, 30)), # 2번째 REM (길어짐)
        (2, (20, 40)), 
        (1, (10, 20)), 
        (5, (30, 40)), # 3번째 REM (더 길어짐)
        (2, (10, 20)),
        (0, (5, 10)),  # 기상 (Wake)
    ]

    current_hour = 23  # 밤 11시 취침 가정
    current_minute = 0
    total_duration_min = 0 # 총 수면 시간(분)
    
    stage_counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0} # 통계용 카운트
    
    # 사이클을 돌면서 Epoch(30초) 단위 데이터 생성
    for stage_code, (min_duration, max_duration) in sleep_cycles:
        # 이 단계에서 머무를 시간(분) 랜덤 결정
        duration_min = random.randint(min_duration, max_duration)
        epochs_count = int(duration_min * 2)  # 1분 = 2 epochs (30초 단위)
        
        for _ in range(epochs_count):
            # 시간 문자열 포맷팅
            start_time_str = f"{current_hour:02d}:{int(current_minute):02d}"
            
            # 30초 증가 로직
            current_minute += 0.5
            if current_minute >= 60:
                current_hour = (current_hour + 1) % 24
                current_minute -= 60
            
            end_time_str = f"{current_hour:02d}:{int(current_minute):02d}"

            formatted_stages.append({
                "startTime": start_time_str,
                "endTime": end_time_str,
                "stage": stage_map[stage_code],
                "level": level_map[stage_code],
                "confidence": round(random.uniform(0.85, 0.99), 2)
            })
            
            # 통계 누적
            stage_counts[stage_code] += 1
            total_duration_min += 0.5

    # 4. 통계 계산 (요약 정보)
    total_epochs = len(formatted_stages)
    
    # 0으로 나누기 방지
    if total_epochs == 0: total_epochs = 1

    summary = {
        "totalSleepTime": int(total_duration_min), # 분 단위
        "sleepEfficiency": 92.5, # (임시 고정값)
        "stages": {
            "wake": round(stage_counts[0] / total_epochs * 100, 1),
            "rem": round(stage_counts[5] / total_epochs * 100, 1),
            "light": round((stage_counts[1] + stage_counts[2]) / total_epochs * 100, 1),
            "deep": round((stage_counts[3] + stage_counts[4]) / total_epochs * 100, 1)
        }
    }

    # 5. 코칭 멘트 생성 (OpenAI 연동 전 Mock 멘트)
    coaching_msg = f"AI 분석 결과, 전체 수면 흐름이 매우 안정적입니다. 특히 깊은 잠(N3/N4) 비율이 {summary['stages']['deep']}%로 신체 회복에 충분한 시간을 확보했습니다. REM 수면 주기도 규칙적으로 나타나고 있어 수면의 질이 우수합니다."

    # 6. 최종 응답 데이터 구성
    # (DB 저장을 위해 딕셔너리로 먼저 만듭니다)
    response_data = {
        "id": "temp_id", # DB 저장 후 업데이트됨
        "date": "2025-05-20", # 실제로는 파일 메타데이터나 오늘 날짜 사용
        "sleepScore": 88,
        "analysisInfo": {
            "modelName": "Hybrid CNN-LSTM (v1.0)",
            "accuracy": 82.4,
            "usedChannels": ["Fpz-Cz", "Pz-Oz"],
            "totalEpochs": total_epochs
        },
        "summary": summary,
        "stages": formatted_stages,
        "aiCoaching": coaching_msg
    }

    # 7. DB 저장 로직 (SQLite)
    try:
        new_report = SleepReport(
            date=response_data["date"],
            sleep_score=response_data["sleepScore"],
            analysis_info=response_data["analysisInfo"],
            summary=response_data["summary"],
            stages=response_data["stages"],
            ai_coaching=response_data["aiCoaching"]
        )
        
        db.add(new_report)
        db.commit()
        db.refresh(new_report) # 저장된 후 생성된 ID(PK)를 가져옴
        
        # 실제 DB ID로 교체
        response_data["id"] = str(new_report.id)
        print(f"✅ DB 저장 완료! Report ID: {new_report.id}")
        
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")
        # DB 저장이 실패해도 프론트엔드에는 결과를 보여줄 수 있도록 함

    # 임시 파일 삭제 (선택 사항)
    # try:
    #     os.remove(file_path)
    # except:
    #     pass

    return response_data

@router.get("/history")
def get_sleep_history(db: Session = Depends(get_db)):
    """
    DB에 저장된 모든 수면 리포트를 날짜 역순(최신순)으로 가져옵니다.
    """
    history = db.query(SleepReport).order_by(SleepReport.date.desc()).all()
    return history