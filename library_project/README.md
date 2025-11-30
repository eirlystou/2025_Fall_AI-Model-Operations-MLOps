# 📚 Library Rental System  
FastAPI + SQLite + Streamlit 기반의 도서 대여·반납 관리 시스템입니다.

---

## 🚀 프로젝트 소개
이 프로젝트는 도서를 **등록, 조회, 수정, 삭제**할 수 있으며,  
사용자가 책을 **대여 및 반납**할 수 있는 간단한 Library Management System입니다.

- Backend: FastAPI  
- Frontend: Streamlit  
- Database: SQLite  
- ORM: SQLAlchemy  
- Data Validation: Pydantic  

---

## 📁 프로젝트 구조
```
library_project/
│
├── backend/
│   ├── database.py   # DB 연결 및 세션 관리
│   ├── models.py     # Book & Loan ORM 모델
│   ├── schemas.py    # Pydantic 데이터 스키마
│   ├── main.py       # FastAPI API 엔드포인트
│   └── library.db    # SQLite DB 파일
│
└── frontend/
    └── app.py        # Streamlit UI

```





---

## ⚙️ 기술 스택

| 영역 | 사용 기술 |
|------|-----------|
| Backend API | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Frontend | Streamlit |
| HTTP Client | requests |

---

## 📌 기능 요약

### 📘 Book 기능
- 도서 등록 (Create)
- 도서 목록 조회 (Read)
- 도서 정보 수정 (Update)
- 도서 삭제 (Delete)

### 📙 Loan 기능
- 도서 대여
- 도서 반납
- 대여/반납 이력 조회

---

## 🔌 API 엔드포인트

### 📘 Book API
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /books | 도서 전체 조회 |
| GET | /books/{id} | 특정 도서 조회 |
| POST | /books | 도서 등록 |
| PUT | /books/{id} | 도서 수정 |
| DELETE | /books/{id} | 도서 삭제 |

### 📙 Loan API
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /loans/borrow | 도서 대여 |
| POST | /loans/{id}/return | 도서 반납 |
| GET | /loans | 대여/반납 이력 조회 |

---

## ▶️ 실행 방법
uvicorn backend.main:app --reload

cd frontend
streamlit run app.py


```bash
pip install fastapi uvicorn sqlalchemy streamlit pydantic
