BEGIN_README

# 📘 강의 자동 시간표 생성 프로젝트

## 🚀 프로젝트 실행 방법

### 1️⃣ 가상환경 생성
```bash
python -m venv myvenv
source myvenv/Scripts/activate     # Windows
# 또는
source myvenv/bin/activate         # macOS/Linux
```

### 2️⃣ 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3️⃣ 백엔드(FastAPI) 실행
```bash
uvicorn backend.main:app --reload
```

### 4️⃣ 프론트엔드(Streamlit) 실행
````bash
streamlit run frontend/app.py
```

---

# 📥 사용 방법 요약
- CSV 파일 업로드  
- “Generate Schedule” 버튼 클릭 → 자동 시간표 생성  
- 학년 / 반(Section) / 학과(Department) 필터링 지원  
- 리스트 + 요일/교시별 시간표 형태로 표시  

---

# 🌱 향후 기능 개선 예정
## 🤖 Gemini LLM 연동
- 자연어로 시간표 수정 요청  
- 충돌 자동 감지 및 해결  
- AI 기반 최적 시간표 추천  

### 예시 요청
- “텍스트&영상처리 강의를 수요일 오전으로 옮겨줘.”  
- “수강 인원이 많은 과목은 큰 강의실로 배정해줘.”  
```


<img width="1823" height="534" alt="image" src="https://github.com/user-attachments/assets/c8e8914c-2f6e-43d9-bde3-71b30be81ea2" />

<img width="1806" height="517" alt="image" src="https://github.com/user-attachments/assets/c92423d8-a73d-482e-b130-9382f65ce318" />

<img width="1820" height="490" alt="image" src="https://github.com/user-attachments/assets/bd69fb64-3796-4eeb-80de-71d501079804" />

<img width="1836" height="745" alt="image" src="https://github.com/user-attachments/assets/6b849d97-c129-4b08-82b4-c16e9efe930a" />




