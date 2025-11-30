# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# --- 공통 설정 ---
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AdventureWorks 대시보드",
    page_icon="🚀",
    layout="wide"
)

# --- 페이지 1: 성과 예측 (Prediction) ---
def page_prediction():
    """고객 구매 예측 페이지 (국가 정보 포함)."""
    st.title("🧑‍💻 고객 구매 여부 예측 (v2 - 국가 포함)")
    st.write("고객의 RFM 값 및 국가를 입력하여 향후 30일 내 구매 여부를 예측합니다.")
    
    st.header("고객 정보 입력")
    
    with st.form(key='customer_prediction_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            recency_input = st.number_input("Recency (경과 일수)", min_value=0, value=30)
        with col2:
            frequency_input = st.number_input("Frequency (구매 횟수)", min_value=1, value=5)
        with col3:
            monetary_input = st.number_input("Monetary (총 구매액)", min_value=0.0, value=1500.50, format="%.2f")
        
        country_input = st.text_input("국가 (Country-Region)", value="United States", help="예: United States, Australia, Germany")
        
        submit_button = st.form_submit_button(label='구매 여부 예측')

    if submit_button:
        # Pydantic 모델의 'alias'와 일치하도록
        # 'Country-Region' (하이픈) 키를 JSON 페이로드에서 사용합니다.
        payload = {
            "Recency_Snapshot": recency_input,
            "Frequency": frequency_input,
            "Monetary": monetary_input,
            "Country-Region": country_input # [SỬA LỖI] 'Country_Region' (밑줄) 대신 하이픈 사용
        }
        
        try:
            url = f"{API_BASE_URL}/predict_customer_purchase"
            with st.spinner("모델 호출 중..."):
                response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("will_purchase_prediction", 0)
                probability = result.get("probability_to_purchase", 0)
                st.success("**예측 성공!**")
                if prediction == 1:
                    st.metric(label="예측 결과", value="구매할 것입니다 (Will Purchase)")
                else:
                    st.metric(label="예측 결과", value="구매하지 않을 것입니다 (Will Not Purchase)")
                st.metric(label="구매 확률", value=f"{probability * 100:.2f}%")
                st.progress(probability)
            else:
                st.error(f"API 오류 (코드: {response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("연결 오류: API에 연결할 수 없습니다. FastAPI 서버(uvicorn)를 실행했는지 확인하세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# --- 페이지 2: 리셀러 데이터 분석 (Reseller EDA) ---
def page_analysis():
    """리셀러 데이터 분석 페이지 렌더링 함수."""
    st.title("📊 리셀러 탐색적 데이터 분석 (EDA)")
    st.write("FastAPI를 통해 리셀러 판매 데이터를 시각화합니다.")
    
    try:
        url = f"{API_BASE_URL}/analysis/reseller_eda"
        with st.spinner("FastAPI에서 분석 데이터 로딩 중..."):
            response = requests.get(url)
        if response.status_code != 200:
            st.error(f"API 데이터 로드 실패 (코드: {response.status_code}): {response.text}")
            return
        data = response.json()
        stats = data.get("summary_stats", {})
        total_sales = stats.get("total_sales", 0)
        total_orders = stats.get("total_orders", 0)
        unique_resellers = stats.get("unique_reseller_types", 0)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("총 매출", f"${total_sales:,.0f}")
        col2.metric("총 거래 수", f"{total_orders:,}")
        col3.metric("리셀러 업종 수", f"{unique_resellers}")
        st.markdown("---")
        st.subheader("업종별 총 매출 (Business Type)")
        df_biz = pd.DataFrame(data.get("sales_by_biz_type", []))
        if not df_biz.empty:
            fig1 = px.bar(df_biz, x='Business Type', y='Sales Amount', title='업종별 매출', text_auto='.2s')
            fig1.update_layout(xaxis_title="업종", yaxis_title="총 매출")
            st.plotly_chart(fig1, use_container_width=True)
        st.subheader("국가별 매출 분포")
        df_country = pd.DataFrame(data.get("sales_by_country", []))
        if not df_country.empty:
            fig2 = px.pie(df_country, names='Country', values='Sales Amount', title='국가별 매출 비중')
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)
        st.subheader("시간에 따른 매출 (월별)")
        df_time = pd.DataFrame(data.get("sales_over_time", []))
        if not df_time.empty:
            fig3 = px.line(df_time, x='Date', y='Sales Amount', title='월별 매출 추이')
            fig3.update_layout(xaxis_title="기간", yaxis_title="총 매출")
            st.plotly_chart(fig3, use_container_width=True)
    except requests.exceptions.ConnectionError:
        st.error("연결 오류: API에 연결할 수 없습니다. FastAPI 서버(uvicorn)를 실행했는지 확인하세요.")
    except Exception as e:
        st.error(f"페이지 렌더링 중 오류 발생: {e}")

# --- 페이지 3: 고객 세분화 (RFM) ---
def page_rfm():
    """고객 RFM 세분화 페이지 렌더링 함수."""
    st.title("🧑‍🤝‍🧑 고객 세분화 (RFM 분석)")
    st.write("FastAPI를 통해 B2C 고객을 Recency, Frequency, Monetary 기준으로 분석합니다.")
    
    try:
        url = f"{API_BASE_URL}/analysis/customer_rfm"
        with st.spinner("FastAPI에서 RFM 데이터 계산 중..."):
            response = requests.get(url)
        if response.status_code != 200:
            st.error(f"API 데이터 로드 실패 (코드: {response.status_code}): {response.text}")
            return
        data = response.json()
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("세그먼트별 고객 수")
            df_counts = pd.DataFrame(data.get("segment_counts", []))
            if not df_counts.empty:
                fig_bar = px.bar(df_counts, x='Segment', y='Count', title="고객 세그먼트 분포", text_auto=True)
                fig_bar.update_layout(xaxis_title="세그먼트", yaxis_title="고객 수")
                st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.subheader("세그먼트별 매출 기여도")
            df_monetary = pd.DataFrame(data.get("segment_monetary", []))
            if not df_monetary.empty:
                fig_tree = px.treemap(df_monetary, path=['Segment'], values='Monetary', title='세그먼트별 총 매출')
                st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("---")
        st.subheader("RFM 분석 데이터 테이블 (매출 상위 100명)")
        df_table = pd.DataFrame(data.get("rfm_table_top100", []))
        if df_table.empty:
            st.info("RFM 테이블 데이터를 찾을 수 없습니다.")
        else:
            columns_order = ['CustomerKey', 'Customer', 'Segment', 'Monetary', 'Frequency', 'Recency', 'RFM_Score']
            display_columns = [col for col in columns_order if col in df_table.columns]
            st.dataframe(df_table[display_columns])
    except requests.exceptions.ConnectionError:
        st.error("연결 오류: API에 연결할 수 없습니다. FastAPI 서버(uvicorn)를 실행했는지 확인하세요.")
    except Exception as e:
        st.error(f"페이지 렌더링 중 오류 발생: {e}")

# --- 사이드바 내비게이션 (메인) ---
st.sidebar.title("페이지 이동 (Navigation)")
page = st.sidebar.radio(
    "페이지 선택:", 
    ("성과 예측", "리셀러 데이터 분석 (EDA)", "고객 세분화 (RFM)")
)

# 선택된 페이지 렌더링
if page == "성과 예측":
    page_prediction()
elif page == "리셀러 데이터 분석 (EDA)":
    page_analysis()
elif page == "고객 세분화 (RFM)":
    page_rfm()