# Chinook 음악 대시보드

Chinook 음악 대시보드는 **FastAPI**를 사용한 백엔드와 **Streamlit**을 사용한 프론트엔드로 구축된 애플리케이션입니다. 이 애플리케이션은 **Chinook**(SQLite) 데이터베이스를 사용하여 아티스트, 앨범, 트랙 및 플레이리스트에 대한 다양한 통계를 시각적으로 제공합니다.

## 📋 프로젝트 설명

이 프로젝트는 다음과 같은 통계를 제공하는 애플리케이션입니다:
- **각 아티스트의 앨범 수**
- **각 앨범의 트랙 수**
- **각 플레이리스트의 트랙 수**
- **트랙 수 기준 상위 아티스트**

이 통계는 막대 차트, 원형 차트, 선 차트 및 영역 차트로 표시됩니다.

## 🔧 사용 기술

- **백엔드**:
  - FastAPI: API 구축을 위한 Python 프레임워크
  - SQLite: 경량 데이터베이스
- **프론트엔드**:
  - Streamlit: 간단한 웹 애플리케이션을 구축할 수 있는 Python 라이브러리
  - Plotly: 다양한 차트를 생성하는 라이브러리

## 🚀 설치

### 백엔드 설치
1. Repository 클론:
    ```bash
    git clone https://github.com/yourusername/Chinook.git
    cd Chinook
    ```

2. **백엔드**에 필요한 라이브러리 설치:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. **FastAPI** 백엔드 실행:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### 프론트엔드 설치
1. **프론트엔드**에 필요한 라이브러리 설치:
    ```bash
    cd frontend
    pip install -r requirements.txt
    ```

2. **Streamlit** 실행:
    ```bash
    streamlit run app.py
    ```

### 데이터베이스 설정
**Chinook_Sqlite.sqlite** 데이터베이스 파일은 **`backend`** 폴더에 있어야 합니다.

## 📊 주요 기능

1. **각 아티스트의 앨범 수**: 각 아티스트가 발매한 앨범의 개수를 표시합니다.
2. **각 앨범의 트랙 수**: 각 앨범에 포함된 트랙의 개수를 표시합니다.
3. **각 플레이리스트의 트랙 수**: 각 플레이리스트에 포함된 트랙의 개수를 표시합니다.
4. **트랙 수 기준 상위 아티스트**: 트랙 수에 기반하여 상위 아티스트 목록을 표시합니다.

## 📁 프로젝트 구조
```
Chinook_Dashboard/
│
├── backend/
│   ├── database.py   # DB 연결
│   ├── schemas.py    # Pydantic 데이터 스키마
│   ├── main.py       # FastAPI API 엔드포인트
│   └── Chinook_Sqlite.sqlite #Database
│
└── frontend/
    └── app.py        # Streamlit UI

```


## 🧑‍💻 사용 방법

1. **백엔드 실행**: 설치가 완료되면 **FastAPI**를 실행합니다:
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    이는 `http://127.0.0.1:8000`에서 API를 실행시킵니다.

2. **프론트엔드 실행**: **Streamlit**을 실행하여 웹 애플리케이션을 표시합니다:
    ```bash
    streamlit run app.py
    ```

