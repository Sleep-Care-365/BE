from pydantic import BaseModel
from typing import List, Optional

# 1. 수면 단계 상세 데이터 (리스트 안에 들어갈 객체)
class SleepStageSchema(BaseModel):
    startTime: str
    endTime: str
    stage: str      # W, N1, N2, N3, N4, R
    level: int      # 그래프 높이용 (0~5)
    confidence: float

# 2. 분석 정보 메타데이터
class AnalysisInfoSchema(BaseModel):
    modelName: str
    accuracy: float
    usedChannels: List[str]
    totalEpochs: int

# [NEW] 3-1. 요약 정보 내부의 stages 구조 정의
class SummaryStagesSchema(BaseModel):
    wake: float
    rem: float
    light: float
    deep: float

# [UPDATE] 3. 수면 요약 정보 (구조 변경됨)
class SleepSummarySchema(BaseModel):
    totalSleepTime: int
    sleepEfficiency: float
    # 예전: deepSleepRatio, remSleepRatio (삭제)
    # 변경: stages 객체 안에 상세 비율 포함
    stages: SummaryStagesSchema

# 4. 최종 리포트 응답 데이터
class SleepReportResponse(BaseModel):
    id: str
    date: str
    sleepScore: int
    analysisInfo: AnalysisInfoSchema
    summary: SleepSummarySchema
    stages: List[SleepStageSchema]
    aiCoaching: str

    class Config:
        from_attributes = True