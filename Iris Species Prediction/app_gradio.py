# app_gradio.py
import gradio as gr     #  Gradio 라이브러리 (웹 UI/UX를 간단히 만드는 도구)
import requests         #  FastAPI 서버와 통신하기 위한 HTTP 요청 라이브러리

#  FastAPI 서버의 예측 엔드포인트 주소
FASTAPI_URL = "http://127.0.0.1:8000/predict/"

#  사용자가 입력한 데이터를 FastAPI 서버로 보내고 예측 결과를 받는 함수
def predict_species(sl, sw, pl, pw):
    # 입력값(꽃의 특징)을 JSON 형식으로 묶기
    payload = {"sl": sl, "sw": sw, "pl": pl, "pw": pw}
    
    # FastAPI 서버에 POST 요청 보내기
    r = requests.post(FASTAPI_URL, json=payload, timeout=10)
    
    # 응답 코드가 200이 아닐 경우 (즉, 에러가 발생한 경우)
    if r.status_code != 200:
        return f"Error {r.status_code}: {r.text}"
    
    # FastAPI 서버에서 받은 JSON 응답 파싱
    data = r.json()
    
    # 예측 결과(숫자)를 실제 꽃 이름으로 변환
    idx2name = {0: "setosa", 1: "versicolor", 2: "virginica"}
    name = idx2name.get(data["prediction"], "unknown")

    #  예측 확률 중 가장 높은 값을 "정확도(%)"로 계산
    confidence = max(data["proba"]) * 100

    #  결과를 간단한 문자열로 반환 (꽃 이름 + 정확도)
    return f"🌸 Prediction: {name}\n🎯 Confidence: {confidence:.2f}%"


#  Gradio 인터페이스 구성 시작
with gr.Blocks(title="Iris Predictor") as demo:
    # 웹 인터페이스 상단의 제목 (Markdown 문법 사용)
    gr.Markdown("### Iris species predictor (calls FastAPI)")
    
    #  첫 번째 행(Row): Sepal 관련 입력 슬라이더
    with gr.Row():
        sl = gr.Slider(4.0, 8.0, value=5.1, step=0.1, label="Sepal length (cm)")  # 꽃받침 길이
        sw = gr.Slider(2.0, 5.0, value=3.5, step=0.1, label="Sepal width (cm)")   # 꽃받침 너비
    
    #  두 번째 행(Row): Petal 관련 입력 슬라이더
    with gr.Row():
        pl = gr.Slider(1.0, 7.0, value=1.4, step=0.1, label="Petal length (cm)")  # 꽃잎 길이
        pw = gr.Slider(0.1, 3.0, value=0.2, step=0.1, label="Petal width (cm)")   # 꽃잎 너비
    
    #  예측 버튼과 결과 창 구성
    btn = gr.Button("Predict")                          # "예측하기" 버튼
    out = gr.Textbox(label="Result", lines=3)           # 결과 출력 상자 (텍스트형)
    
    # 버튼 클릭 시 predict_species 함수를 호출하고 결과를 출력창에 표시
    btn.click(predict_species, inputs=[sl, sw, pl, pw], outputs=out)


#  Gradio 앱 실행 부분
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
