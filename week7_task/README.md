# 🧭 AdventureWorks 판매 분석 및 예측 대시보드
본 프로젝트는 **AdventureWorks 판매 데이터(.xlsx)**를 분석하고, 머신러닝 모델을 구축하여 고객의 미래 구매 여부를 예측하는 **풀스택 애플리케이션**입니다.  
백엔드는 **FastAPI**로 API를 제공하며, 프론트엔드는 **Streamlit**을 사용하여 구축된 **대화형 대시보드**입니다.
## 🚀 주요 기능
### 🔹 데이터 파이프라인  
- Excel 시트(Customer_data, Reseller_data 등)를 단일 SQLite 데이터베이스(`AdventureWorks-Sales.sqlite3`)로 가져옵니다.
### 🔹 백엔드 API (FastAPI)  
3개의 주요 엔드포인트를 제공합니다:  
| Endpoint | 설명 |  
|-----------|------|  
| `/predict_customer_purchase` | 고객의 RFM 및 국가 정보를 기반으로 미래 구매 여부를 예측합니다. (**XGBoost 분류 모델**) |  
| `/analysis/reseller_eda` | 리셀러(Reseller) 관련 **탐색적 데이터 분석(EDA)** 데이터를 제공합니다. |  
| `/analysis/customer_rfm` | 고객(Customer) **RFM 세분화 분석** 데이터를 제공합니다. |
### 🔹 프론트엔드 대시보드 (Streamlit)
- **성과 예측:** API를 호출하여 실시간 고객 구매 확률 예측  
- **리셀러 데이터 분석:** 매출, 업종, 국가별 시각화  
- **고객 세분화 (RFM):** B2C 고객을 RFM 기준으로 시각화
## 🛠️ 사용된 기술 스택
| 분류 | 기술 |  
|------|------|  
| 언어 | Python 3.10+ |  
| 백엔드 | FastAPI, Uvicorn |  
| 프론트엔드 | Streamlit |  
| 머신러닝 | Scikit-learn, XGBoost |  
| 데이터 처리 | Pandas, NumPy |  
| 데이터베이스 | SQLite3 |  
| 시각화 | Plotly |
## 📁 프로젝트 구조 및 실행 방법
```plaintext
/Your_Project_Folder/
│
├── /data/
│   ├── AdventureWorks-Sales.xlsx      # (1) 원본 Excel 데이터 파일
│   └── AdventureWorks-Sales.sqlite3   # (2) 생성된 DB 파일
│
├── /models/
│   ├── model.joblib                   # (4) 학습된 XGBoost 모델
│   └── preprocessor.joblib            # (4) 학습된 전처리기
│
├── app.py                             # Streamlit 프론트엔드
├── main.py                            # FastAPI 백엔드
├── train.py                           # (3) 모델 학습 스크립트
├── import_excel_to_db.py              # (2) DB 임포트 스크립트
├── requirements.txt                   # 필요한 라이브러리
└── README.md                          # 현재 파일
## ⚙️ 설치 및 실행 방법

### 1️⃣ 환경 설정
프로젝트 폴더로 이동합니다.
(선택 사항) 가상 환경을 생성하고 활성화합니다:
```bash
python -m venv venv
.\venv\Scripts\activate
```
필요한 라이브러리를 설치합니다:
```bash
pip install -r requirements.txt
```
💡 만약 requirements.txt 파일이 없다면 아래 명령어 실행:
```bash
pip install pandas scikit-learn xgboost fastapi uvicorn[standard] joblib openpyxl streamlit requests plotly
```

### 2️⃣ 데이터베이스 생성
원본 Excel 파일(AdventureWorks-Sales.xlsx)을 /data/ 폴더에 넣고 아래 실행:
```bash
python import_excel_to_db.py
```
✅ 성공 시 /data/AdventureWorks-Sales.sqlite3 파일이 생성됩니다.

### 3️⃣ 머신러닝 모델 학습
```bash
python train.py
```
✅ 성공 시 /models/ 폴더에 model.joblib 및 preprocessor.joblib 생성

### 4️⃣ 애플리케이션 실행 (2개의 터미널 필요)

🟢 터미널 1: FastAPI 백엔드 실행

```bash
uvicorn main:app --reload
```

API: http://127.0.0.1:8000

API 문서: http://127.0.0.1:8000/docs

🔵 터미널 2: Streamlit 프론트엔드 실행

```bash
streamlit run app.py
```

Streamlit 대시보드: http://127.0.0.1:8501
 (또는 다른 포트)
