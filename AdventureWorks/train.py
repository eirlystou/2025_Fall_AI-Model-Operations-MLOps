# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import os
import datetime
import numpy as np

# --- 상수 정의 ---
DB_PATH = os.path.join('data', 'AdventureWorks-Sales.sqlite3')
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'model.joblib')
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'preprocessor.joblib')
PREDICTION_WINDOW_DAYS = 30

def load_data(db_path):
    """(B2C 고객) SQLite에서 데이터 로드. [CẬP NHẬT] Customers 테이블 추가."""
    print("데이터 로딩 중 (B2C 고객, 날짜, 고객 정보)...")
    if not os.path.exists(db_path):
        print(f"오류: '{db_path}'에서 데이터베이스 파일을 찾을 수 없습니다.")
        return None, None
    try:
        conn = sqlite3.connect(db_path)
        # B2C 판매 데이터 로드
        df_sales = pd.read_sql("SELECT CustomerKey, OrderDateKey, [Sales Amount] FROM Sales WHERE ResellerKey = -1 AND CustomerKey != -1", conn)
        df_dates = pd.read_sql("SELECT DateKey, Date FROM Date", conn)
        
        # 고객 테이블 로드 (Country-Region 특성 사용)
        df_customers = pd.read_sql("SELECT CustomerKey, [Country-Region] FROM Customers WHERE CustomerKey != -1", conn)
        
        conn.close()
        
        df_merged = pd.merge(df_sales, df_dates, left_on='OrderDateKey', right_on='DateKey')
        df_merged['Date'] = pd.to_datetime(df_merged['Date'])
        
        # 이제 sales_data와 customers_data를 반환
        return df_merged[['CustomerKey', 'Date', 'Sales Amount']], df_customers
    except Exception as e:
        print(f"데이터 로딩 오류: {e}")
        return None, None

def feature_engineering(df_sales_data, df_customers):
    """특성(X = RFM + 인구통계) 및 타겟(Y = Will_Purchase) 생성."""
    print("피처 엔지니어링 수행 중 (RFM + 국가 정보)...")
    
    # 1. "현재" 및 "예측 창" 정의
    max_date = df_sales_data['Date'].max()
    snapshot_date = max_date - datetime.timedelta(days=PREDICTION_WINDOW_DAYS)
    
    # 2. 특성 (X) 생성 - 과거 데이터 (snapshot_date 이전)
    df_features_sales = df_sales_data[df_sales_data['Date'] <= snapshot_date]
    
    # RFM 계산
    rfm_features = df_features_sales.groupby('CustomerKey').agg(
        Recency_Snapshot=('Date', lambda x: (snapshot_date - x.max()).days),
        Frequency=('Date', 'nunique'),
        Monetary=('Sales Amount', 'sum')
    ).reset_index()

    # 3. 타겟 (Y) 생성 - 미래 데이터 (prediction_window 내부)
    df_target_window = df_sales_data[df_sales_data['Date'] > snapshot_date]
    customers_who_purchased = df_target_window['CustomerKey'].unique()
    
    # 4. RFM 특성과 고객 특성(Country-Region) 결합
    #  rfm_features에 df_customers 결합
    rfm_features = pd.merge(rfm_features, df_customers, on='CustomerKey', how='left')
    
    # 5. 최종 데이터 테이블 생성
    rfm_features['Will_Purchase'] = rfm_features['CustomerKey'].isin(customers_who_purchased).astype(int)
    rfm_features.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    return rfm_features

def train_model():
    """분류 모델 학습을 위한 메인 함수."""
    
    # 1. 데이터 로드
    # 2개의 DF 로드
    df_raw_sales, df_raw_customers = load_data(DB_PATH)
    if df_raw_sales is None or df_raw_customers is None:
        return

    # 2. 피처 엔지니어링
    # 2개의 DF 전달
    df_data = feature_engineering(df_raw_sales, df_raw_customers)
    if df_data is None:
        print("피처를 생성할 수 없습니다.")
        return

    # 3. X와 y 정의
    # X에 'Country-Region' 추가
    features_list = ['Recency_Snapshot', 'Frequency', 'Monetary', 'Country-Region']
    X = df_data[features_list]
    y = df_data['Will_Purchase']
    
    if y.nunique() < 2:
        print("오류: 타겟 데이터에 클래스가 하나만 존재합니다. 분류 모델을 학습할 수 없습니다.")
        return

    # 4. 열 정의
    # 숫자형/범주형 특성 분리
    numerical_features = ['Recency_Snapshot', 'Frequency', 'Monetary']
    categorical_features = ['Country-Region']
    
    # 5. 전처리기 파이프라인 구성
    
    # 숫자형 파이프라인 (변경 없음)
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # 범주형 파이프라인 (새로 추가)
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Missing')), # 결측치를 'Missing'으로 채움
        ('onehot', OneHotEncoder(handle_unknown='ignore')) # 원-핫 인코딩
    ])
    
    # ColumnTransformer가 이제 두 파이프라인을 모두 처리
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # 6. 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 7. 전처리기 학습
    print("전처리기 학습 중 (RFM + 국가)...")
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # 8. 모델 학습 (XGBClassifier)
    print("XGBClassifier 모델 학습 중...")
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss', scale_pos_weight=scale_pos_weight)
    model.fit(X_train_processed, y_train)
    
    # 9. 모델 평가
    y_pred = model.predict(X_test_processed)
    y_pred_proba = model.predict_proba(X_test_processed)[:, 1]
    
    print("\n--- 모델 평가 (분류) ---")
    print(f"Accuracy (정확도): \t{accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision (정밀도): \t{precision_score(y_test, y_pred):.4f}")
    print(f"Recall (재현율): \t\t{recall_score(y_test, y_pred):.4f}")
    print(f"F1-Score (F1 점수): \t{f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC Score (AUC): \t{roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # 10. 모델 및 전처리기 저장
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    
    print(f"\n모델 저장 완료: {MODEL_PATH}")
    print(f"전처리기 저장 완료: {PREPROCESSOR_PATH}")

if __name__ == "__main__":
    train_model()