AdventureWorks 판매 분석 및 예측 대시보드

본 프로젝트는 AdventureWorks 판매 데이터(.xlsx)를 분석하고, 머신러닝 모델을 구축하여 고객의 미래 구매 여부를 예측하는 풀스택 애플리케이션입니다.

백엔드는 FastAPI를 사용하여 API를 제공하며, 프론트엔드는 Streamlit을 사용하여 구축된 대화형 대시보드입니다.

🚀 주요 기능

데이터 파이프라인: Excel 시트(Customer_data, Reseller_data 등)를 단일 SQLite 데이터베이스(AdventureWorks-Sales.sqlite3)로 가져옵니다.

백엔드 API (FastAPI): 3개의 주요 엔드포인트를 제공합니다.

/predict_customer_purchase: 고객의 RFM 및 국가 정보를 기반으로 미래 구매 여부를 예측합니다. (XGBoost 분류 모델)

/analysis/reseller_eda: 리셀러(Reseller) 관련 EDA(탐색적 데이터 분석) 데이터를 제공합니다.

/analysis/customer_rfm: 고객(Customer) RFM 세분화 분석 데이터를 제공합니다.

프론트엔드 대시보드 (Streamlit): 3페이지로 구성된 인터랙티브 웹 앱.

성과 예측: API를 호출하여 실시간으로 고객 구매 확률을 예측합니다.

리셀러 데이터 분석: 리셀러의 매출, 업종, 국가별 데이터를 시각화합니다.

고객 세분화 (RFM): B2C 고객을 RFM 기준으로 세분화하고 시각화합니다.

🛠️ 사용된 기술 스택

Python 3.10+

백엔드 (API): FastAPI, Uvicorn

프론트엔드 (UI): Streamlit

머신러닝: Scikit-learn, XGBoost

데이터 처리: Pandas, NumPy

데이터베이스: SQLite3

시각화: Plotly

📁 프로젝트 구조

/Your_Project_Folder/
|
|-- /data/
|   |-- AdventureWorks-Sales.xlsx     (1. 원본 Excel 데이터 파일)
|   |-- AdventureWorks-Sales.sqlite3  (2. 생성된 DB 파일)
|
|-- /models/
|   |-- model.joblib                (4. 학습된 XGBoost 모델)
|   |-- preprocessor.joblib         (4. 학습된 전처리기)
|
|-- app.py                          (Streamlit 프론트엔드)
|-- main.py                         (FastAPI 백엔드)
|-- train.py                        (3. 모델 학습 스크립트)
|-- import_excel_to_db.py           (2. DB 임포트 스크립트)
|-- requirements.txt                (필요한 라이브러리)
|-- README.md                       (현재 파일)


⚙️ 설치 및 실행 방법

1단계: 환경 설정

프로젝트 폴더로 이동합니다.

(선택 사항) 가상 환경을 생성하고 활성화합니다.

python -m venv venv
.\venv\Scripts\activate


필요한 라이브러리를 설치합니다.

pip install -r requirements.txt


(만약 requirements.txt 파일이 없다면, pip install pandas scikit-learn xgboost fastapi uvicorn[standard] joblib openpyxl streamlit requests plotly를 실행하세요.)

2단계: 데이터베이스 생성

원본 데이터 파일인 AdventureWorks-Sales.xlsx를 /data/ 폴더 안에 넣습니다.

아래 명령어를 실행하여 Excel 데이터를 SQLite 데이터베이스로 변환합니다.

python import_excel_to_db.py


(이 명령어가 성공하면 /data/ 폴더 안에 AdventureWorks-Sales.sqlite3 파일이 생성됩니다.)

3단계: 머신러닝 모델 학습

아래 명령어를 실행하여 머신러닝 모델을 학습시킵니다.

python train.py


(이 명령어가 성공하면 /models/ 폴더 안에 model.joblib와 preprocessor.joblib 파일이 생성됩니다.)

4단계: 애플리케이션 실행 (2개의 터미널 필요)

애플리케이션을 실행하려면 2개의 터미널을 동시에 열어야 합니다.

1. 🟢 터미널 1: 백엔드 (FastAPI) 실행

uvicorn main:app --reload


API가 http://127.0.0.1:8000에서 실행됩니다.

API 문서는 http://127.0.0.1:8000/docs에서 확인할 수 있습니다.

2. 🔵 터미널 2: 프론트엔드 (Streamlit) 실행

streamlit run app.py


Streamlit 대시보드가 http://127.0.0.1:8501 (또는 다른 포트)에서 자동으로 열립니다.

이제 브라우저에서 Streamlit 대시보드를 사용하여 프로젝트를 확인할 수 있습니다.