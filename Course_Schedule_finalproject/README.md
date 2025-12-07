# 📘 강의 시간표 자동 편성 프로젝트

## 🚀 프로젝트 실행 방법
1️⃣ **가상환경 생성**
```bash
python -m venv myvenv
source myvenv/Scripts/activate     # Windows
# 또는
source myvenv/bin/activate         # macOS/Linux

## 라이브러리 설치
pip install -r requirements.txt

##백엔드(FastAPI) 실행
uvicorn backend.main:app --reload


##프론트엔드(Streamlit) 실행
streamlit run frontend/app.py
##📥 사용 방법 요약

CSV 파일 업로드

“Generate Schedule” 버튼 클릭 → 자동 시간표 생성

학년 / 반(Section) / 학과(Department) 필터링 지원

리스트 + 요일/교시별 시간표 형태로 표시

##🌱 향후 기능 개선 예정

Gemini LLM 연동

자연어로 시간표 수정 요청

충돌 자동 감지 및 해결

AI 기반 최적 시간표 추천

예시 요청:

“텍스트&영상처리 강의를 수요일 오전으로 옮겨줘.”
“수강 인원이 많은 과목은 큰 강의실로 배정해줘.”
