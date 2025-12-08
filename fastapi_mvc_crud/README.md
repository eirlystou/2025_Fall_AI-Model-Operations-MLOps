# 📘 FastAPI MVC CRUD 프로젝트 (No ORM) (week10_Chauvrusa_05)

이 프로젝트는 **FastAPI**를 기반으로 **MVC(Model – Service – Router)** 패턴을 적용하여 구현한 RESTful API입니다.  
ORM(SQLAlchemy)을 사용하지 않고, **SQLite + 순수 SQL**과 **Pandas PSV 로딩**을 활용하여 CRUD 기능을 직접 구현합니다.

---

## 🚀 주요 특징

- Creatures / Explorers CRUD 기능 제공
- MVC 구조에 기반한 명확한 계층 분리
  - **models/** → Pydantic 모델 정의
  - **services/** → 비즈니스 로직 & SQL CRUD 처리
  - **routers/** → API 엔드포인트 정의
  - **data/** → 데이터베이스 초기화 및 PSV 파일 로딩
- SQLAlchemy 등 ORM 미사용
- `creatures.psv`, `explorers.psv` 파일에서 초기 데이터 로딩
- 실행 시 SQLite DB 자동 생성

---

## 📁 프로젝트 구조
``` bash
project/
│── main.py
│── README.md
│── creatures.psv
│── explorers.psv
│
├── models/
│ ├── creature.py
│ └── explorer.py
│
├── services/
│ ├── creature_service.py
│ └── explorer_service.py
│
├── routers/
│ ├── creature.py
│ └── explorer.py
│
└── data/
├── database.py
└── psv_loader.py
```

---

## 🛠 설치 방법

### 1️⃣ 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate (Linux/Mac)
venv\Scripts\activate (Windows)
```

### 2️⃣ 라이브러리 설치

```bash
pip install fastapi uvicorn pandas
```

---

## ▶️ 실행 방법

```bash
uvicorn main:app --reload
```

---

## 📚 API 문서

FastAPI 서버 실행 후 아래 주소로 접속:

- Swagger UI → http://localhost:8000/docs  
- ReDoc → http://localhost:8000/redoc  

---

## ✨ 예시 요청 바디 (Creatures)

```json
{
  "name": "Dragon",
  "habitat": "Mountain",
  "power": 95
}
```
---
## 📌 참고사항

app.db 파일은 서버 실행 시 자동 생성됩니다.

데이터베이스 구조를 변경한 경우, app.db를 삭제 후 재실행해야 합니다.

모든 CRUD는 SQL로 직접 구현되며 ORM은 사용하지 않습니다.

---

## 🧩 요약

이 프로젝트는 FastAPI의 핵심 개념들을 연습하는 데 초점을 맞춥니다:

- 모듈화 구조 설계  
- Dependency Injection  
- Pydantic 데이터 모델링  
- RESTful API 구축  
- 순수 SQL 기반 CRUD 구현  
