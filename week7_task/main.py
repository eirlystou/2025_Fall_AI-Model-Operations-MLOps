# -*- coding: utf-8 -*-
import fastapi
import joblib
import pandas as pd
from pydantic import BaseModel, Field
import os
import sqlite3
import datetime
import re
import numpy as np

# --- FastAPI 앱 초기화 ---
app = fastapi.FastAPI(title="AdventureWorks API (모델 + 분석)")

# --- 설정 및 모델 로드 ---
MODEL_PATH = os.path.join('models', 'model.joblib')
PREPROCESSOR_PATH = os.path.join('models', 'preprocessor.joblib')
DB_PATH = os.path.join('data', 'AdventureWorks-Sales.sqlite3')

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("고객 구매 예측 모델(v2) 및 전처리기 로드 성공.")
except FileNotFoundError:
    print(f"오류: '{MODEL_PATH}' 또는 '{PREPROCESSOR_PATH}'을(를) 찾을 수 없습니다.")
    print("먼저 'python train.py'를 실행하여 모델을 학습시키세요.")
    model = None
    preprocessor = None
except Exception as e:
    print(f"모델 로드 중 예기치 않은 오류 발생: {e}")
    model = None
    preprocessor = None

# --- DB 연결 헬퍼 함수 ---
def get_db_connection():
    """SQLite DB 연결 생성."""
    if not os.path.exists(DB_PATH):
        raise fastapi.HTTPException(status_code=500, detail="오류: 'data/AdventureWorks-Sales.sqlite3' 파일을 찾을 수 없습니다.")
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"DB 연결 오류: {e}")

# ===============================================
# 1. API 예측 (CUSTOMER PURCHASE PREDICTION)
# ===============================================

class CustomerInput(BaseModel):
    """  Pydantic 모델이 JSON의 'Country-Region'(하이픈)을 허용하도록 수정 """
    Recency_Snapshot: int = Field(..., example=30)
    Frequency: int = Field(..., example=5)
    Monetary: float = Field(..., example=1500.50)
    
    # Python 변수명은 'Country_Region' (밑줄)을 사용합니다.
    # 하지만 'alias'를 사용해 JSON 입력으로 'Country-Region' (하이픈)을 받도록 합니다.
    Country_Region: str = Field(..., alias="Country-Region", example="United States")

    class Config:
        allow_population_by_field_name = True # 'Country_Region' (밑줄)로도 입력을 허용

class CustomerPredictionOut(BaseModel):
    """구매 예측 결과"""
    will_purchase_prediction: int
    probability_to_purchase: float

@app.post("/predict_customer_purchase", 
          summary="고객의 구매 여부 예측 (신규)",
          response_model=CustomerPredictionOut,
          tags=["1. Prediction (Customer)"])
async def predict_customer_purchase(data: CustomerInput):
    """
     고객의 RFM 및 국가를 기반으로 구매 여부를 예측합니다.
    """
    if model is None or preprocessor is None:
        raise fastapi.HTTPException(status_code=500, detail="모델이 학습되지 않았습니다.")
    
    try:
        # data.dict(by_alias=True)를 사용하여
        # {'Country-Region': 'USA'} (하이픈)을 포함한 딕셔너리를 생성합니다.
        input_data_dict = data.dict(by_alias=True)
        
        # 이제 이 DataFrame은 train.py가 학습한 것과 동일한
        # 'Country-Region' (하이픈) 열 이름을 갖게 됩니다.
        input_df = pd.DataFrame([input_data_dict], columns=['Recency_Snapshot', 'Frequency', 'Monetary', 'Country-Region'])
        
        # 이제 전처리기가 올바르게 작동합니다.
        processed_input = preprocessor.transform(input_df)
        prediction = model.predict(processed_input)
        probability = model.predict_proba(processed_input)
        
        prediction_int = int(prediction[0])
        probability_float = float(probability[0][1])
        
        return {
            "will_purchase_prediction": prediction_int,
            "probability_to_purchase": probability_float
        }
    except Exception as e:
        # DataFrame.columns 관련 오류가 발생하면 여기에서 잡힙니다.
        raise fastapi.HTTPException(status_code=400, detail=f"예측 중 오류 발생: {e}")

# ===============================================
# 2. API 분석 (ANALYSIS - EDA)
# ===============================================

@app.get("/analysis/reseller_eda", 
         summary="리셀러 EDA 데이터 가져오기",
         tags=["2. Analysis (EDA)"])
async def get_reseller_eda_data():
    """(API) 리셀러 분석 데이터를 JSON으로 계산하고 반환합니다."""
    conn = get_db_connection()
    try:
        df_sales = pd.read_sql("SELECT OrderDateKey, ResellerKey, SalesTerritoryKey, [Sales Amount] FROM Sales WHERE ResellerKey != -1", conn)
        df_resellers = pd.read_sql("SELECT ResellerKey, [Business Type] FROM Resellers", conn)
        df_territories = pd.read_sql("SELECT SalesTerritoryKey, Country FROM Territories", conn)
        df_dates = pd.read_sql("SELECT DateKey, Date FROM Date", conn)
        conn.close()
        merged_df = pd.merge(df_sales, df_resellers, on='ResellerKey')
        merged_df = pd.merge(merged_df, df_territories, on='SalesTerritoryKey')
        merged_df = pd.merge(merged_df, df_dates, left_on='OrderDateKey', right_on='DateKey')
        merged_df['Date'] = pd.to_datetime(merged_df['Date'])
        total_sales = df_sales['Sales Amount'].sum()
        total_orders = len(df_sales)
        unique_resellers = df_resellers['Business Type'].nunique()
        sales_by_biz = merged_df.groupby('Business Type')['Sales Amount'].sum().reset_index().sort_values(by='Sales Amount', ascending=False)
        sales_by_country = merged_df.groupby('Country')['Sales Amount'].sum().reset_index()
        df_time = merged_df.set_index('Date').resample('M')['Sales Amount'].sum().reset_index()
        df_time['Date'] = df_time['Date'].astype(str)
        return {
            "summary_stats": {"total_sales": total_sales, "total_orders": total_orders, "unique_reseller_types": unique_resellers},
            "sales_by_biz_type": sales_by_biz.to_dict('records'),
            "sales_by_country": sales_by_country.to_dict('records'),
            "sales_over_time": df_time.to_dict('records')
        }
    except Exception as e:
        if conn: conn.close()
        raise fastapi.HTTPException(status_code=500, detail=f"분석 처리 중 오류: {e}")

# ===============================================
# 3. API 세분화 (RFM) - 변경 없음
# ===============================================

def get_rfm_segments(rfm_df):
    """RFM 세그먼트 할당 헬퍼 함수."""
    segment_map = {
        r'[4-5][4-5][4-5]': 'Champions (챔피언)',
        r'[3-5][3-5][1-3]': 'Loyal Customers (충성 고객)',
        r'[3-4][1-2][3-5]': 'Potential Loyalist (잠재적 충성 고객)',
        r'5[1-2][1-2]': 'New Customers (신규 고객)',
        r'[1-2][3-5][3-5]': 'At Risk Customers (이탈 위험 고객)',
        r'[3-4][1-2][1-2]': 'Need Attention (관심 필요)',
        r'[1-2][1-2][3-5]': 'Hibernating (휴면 고객)',
        r'[1-2][1-2][1-2]': 'Lost (이탈 고객)'
    }
    def assign_segment(rfm_score):
        for regex, segment in segment_map.items():
            if re.match(regex, rfm_score):
                return segment
        return 'Other (기타)'
    rfm_df['Segment'] = rfm_df['RFM_Score'].apply(assign_segment)
    return rfm_df

@app.get("/analysis/customer_rfm", 
         summary="고객 RFM 세분화 데이터 가져오기",
         tags=["3. Analysis (RFM)"])
async def get_customer_rfm_data():
    """(API) RFM 데이터를 JSON으로 계산하고 반환합니다."""
    conn = get_db_connection()
    try:
        df_sales = pd.read_sql("SELECT CustomerKey, OrderDateKey, [Sales Amount] FROM Sales WHERE ResellerKey = -1 AND CustomerKey != -1", conn)
        df_dates = pd.read_sql("SELECT DateKey, Date FROM Date", conn)
        df_customers = pd.read_sql("SELECT CustomerKey, Customer FROM Customers", conn)
        conn.close()
        df_customer = pd.merge(df_sales, df_dates, left_on='OrderDateKey', right_on='DateKey')
        df_customer['Date'] = pd.to_datetime(df_customer['Date'])
        snapshot_date = df_customer['Date'].max() + datetime.timedelta(days=1)
        rfm_df = df_customer.groupby('CustomerKey').agg(
            Recency=('Date', lambda x: (snapshot_date - x.max()).days),
            Frequency=('Date', 'nunique'),
            Monetary=('Sales Amount', 'sum')
        ).reset_index()
        r_labels = range(5, 0, -1); f_labels = range(1, 6); m_labels = range(1, 6)
        rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=r_labels, duplicates='drop').astype(int)
        rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 5, labels=f_labels).astype(int)
        rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'].rank(method='first'), 5, labels=m_labels).astype(int)
        rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
        rfm_df = get_rfm_segments(rfm_df)
        rfm_df = pd.merge(rfm_df, df_customers, on='CustomerKey', how='left')
        rfm_df_top100 = rfm_df.sort_values(by='Monetary', ascending=False).head(100)
        segment_counts = rfm_df['Segment'].value_counts().reset_index(name='Count')
        segment_monetary = rfm_df.groupby('Segment')['Monetary'].sum().reset_index()
        return {
            "segment_counts": segment_counts.to_dict('records'),
            "segment_monetary": segment_monetary.to_dict('records'),
            "rfm_table_top100": rfm_df_top100.to_dict('records')
        }
    except Exception as e:
        if conn: conn.close()
        raise fastapi.HTTPException(status_code=500, detail=f"RFM 처리 중 오류: {e}")