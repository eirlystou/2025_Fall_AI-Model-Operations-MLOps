# api.py
from fastapi import FastAPI                     # FastAPI: Python 기반의 고성능 웹 API 프레임워크
from pydantic import BaseModel, Field           # 데이터 검증용 모델 정의 (입력값 타입 보장)
from typing import List                         # 여러 개의 입력을 처리할 때 리스트 타입 사용
import pickle, numpy as np                      # pickle: 모델 불러오기 / numpy: 수치 계산용
from fastapi.middleware.cors import CORSMiddleware  # CORS 설정 (다른 도메인 요청 허용)

# 저장된 모델 파일 경로
MODEL_PATH = "iris_model.pkl"

# 사전에 학습된 모델(.pkl 파일) 로드
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# FastAPI 앱 생성
app = FastAPI(title="Iris Model API", version="1.0")

# Gradio나 JS 프론트엔드가 localhost에서 접근할 수 있도록 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 모든 출처(origin) 허용
    allow_credentials=True,
    allow_methods=["*"],        # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],        # 모든 헤더 허용
)

# 입력 데이터 구조 정의 (단일 예측용)
class IrisInput(BaseModel):
    sl: float = Field(..., description="sepal length")   # 꽃받침 길이, "..." bắt buộc phải có giá trị
    sw: float = Field(..., description="sepal width")    # 꽃받침 너비
    pl: float = Field(..., description="petal length")   # 꽃잎 길이
    pw: float = Field(..., description="petal width")    # 꽃잎 너비


# 기본 엔드포인트 (GET 요청용)
@app.get("/")
def root():
    # 기본 메시지 반환 — 브라우저에서 "/" 접근 시 안내 문구 표시
    return {"ok": True, "message": "Use POST /predict"}

# 단일 예측 엔드포인트 (POST 요청)
@app.post("/predict/")
def predict(item: IrisInput):
    # 입력값을 numpy 배열 형태로 변환 (모델 입력 형식에 맞추기)
    X = np.array([[item.sl, item.sw, item.pl, item.pw]])

    # 모델 예측 수행
    pred = int(model.predict(X)[0])               # 예측된 클래스 인덱스 (0, 1, 2)
    proba = model.predict_proba(X)[0].tolist()    # 각 클래스별 확률값

    # JSON 형태로 결과 반환
    return {"prediction": pred, "proba": proba}

