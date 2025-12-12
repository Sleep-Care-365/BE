# Sleep Care 365 - Backend Server

Sleep Care 365의 백엔드 서버 리포지토리입니다.  
사용자의 수면 데이터를 수집·저장하고, 수면 품질 알고리즘을 통해 분석된 리포트를 프론트엔드 클라이언트에 제공합니다.  
RESTful API 아키텍처를 따르며 데이터 무결성과 효율적인 쿼리 처리를 최우선으로 설계되었습니다.

---

## 🛠 Tech Stack

| **Category** | **Technology**                      |
| ------------ | ----------------------------------- |
| Runtime      | Node.js                             |
| Framework    | Express.js                          |
| Database     | SQLite / MySQL                      |
| ORM / Query  | SQL / Query Builder                 |
| Architecture | MVC Pattern (Model-View-Controller) |

---

## 📂 Project Structure

BE/
├── src
│ ├── config # 데이터베이스 연결 설정
│ ├── controllers # 요청 처리 및 비즈니스 로직 수행
│ ├── models # 데이터베이스 스키마 및 쿼리 관리
│ ├── routes # API 라우팅 정의
│ ├── services # 수면 분석 알고리즘 및 데이터 가공
│ └── utils # 공통 유틸리티 함수
├── app.js # Entry Point
└── package.json # 의존성 관리

---

## 📡 API Documentation

1. **수면 기록 조회 (Get Sleep History)**  
   사용자의 일별 수면 기록, 수면 단계(Deep, Light, REM), 수면 효율 및 수면 점수를 반환합니다.

- **Endpoint:** GET /api/sleep/history
- **Description:** 대시보드 차트 및 히트맵을 위한 시계열 데이터 제공

**Response Example (JSON):**
[
{
"id": 1024,
"user_id": "user_01",
"date": "2025-05-20T00:00:00.000Z",
"sleep_score": 88,
"summary": {
"totalSleepTime": 480,
"sleepEfficiency": 92,
"stages": {
"deep": 25,
"light": 55,
"rem": 20
}
}
},
{
"id": 1025,
"user_id": "user_01",
"date": "2025-05-21T00:00:00.000Z",
"sleep_score": 76,
"summary": {
"totalSleepTime": 420,
"sleepEfficiency": 85,
"stages": {
"deep": 15,
"light": 60,
"rem": 25
}
}
}
]

---

## 💾 Database Schema

**Table:** sleep_records

| Column Name      | Type      | Description             |
| ---------------- | --------- | ----------------------- |
| id               | INT (PK)  | 레코드 고유 ID          |
| user_id          | VARCHAR   | 사용자 식별자           |
| date             | DATETIME  | 수면 날짜               |
| total_sleep_time | INT       | 총 수면 시간(분)        |
| sleep_efficiency | INT       | 수면 효율 (%)           |
| sleep_score      | INT       | 알고리즘 기반 수면 점수 |
| created_at       | TIMESTAMP | 데이터 생성 시간        |

※ 수면 단계 데이터는 확장성을 위해 별도 테이블 또는 JSON 컬럼으로 관리 가능.

---

## 🚀 Getting Started

1. **Installation**
   npm install

2. **Environment Setup (.env)**  
   PORT=8080  
   DB_HOST=localhost  
   DB_USER=root  
   DB_PASSWORD=your_password  
   DB_DATABASE=sleep_care_db

3. **Run Server**  
   개발 모드:
   npm run dev

   프로덕션 모드:
   npm start

---

## ⚙️ Core Logic

- **Data Validation:** 타입·범위 검증
- **Score Algorithm:** 수면 시간/효율/깊은 잠 비율 가중 합산
- **Error Handling:** 표준화된 에러 응답 처리

---

© 2025 Sleep Care 365 Project. All Rights Reserved.
