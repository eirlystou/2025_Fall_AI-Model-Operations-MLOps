# frontend/app.py
import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="강의 시간표 및 강의실 배정 시스템",
    layout="wide",
)
st.title("📚 강의 시간표 및 강의실 배정 시스템")

# ----------------- SESSION STATE ----------------- #

if "csv_uploaded" not in st.session_state:
    st.session_state.csv_uploaded = False

if "schedule_df" not in st.session_state:
    st.session_state.schedule_df = pd.DataFrame()


# ----------------- 헬퍼: 백엔드에서 시간표 받아오기 ----------------- #

def fetch_schedule_from_backend():
    """백엔드 /schedule API 호출"""
    try:
        resp = requests.get(f"{BACKEND_URL}/schedule")
    except Exception as e:
        st.error(f"백엔드 /schedule 호출 실패: {e}")
        st.session_state.schedule_df = pd.DataFrame()
        return

    if resp.status_code != 200:
        st.error(f"시간표 조회 오류: {resp.status_code} - {resp.text}")
        st.session_state.schedule_df = pd.DataFrame()
        return

    data = resp.json()
    if not data:
        st.session_state.schedule_df = pd.DataFrame()
        return

    # 테이블 변환
    rows = []
    for item in data:
        course = item["course"]
        classroom = item["classroom"]

        section = course.get("section")
        department = course.get("department")

        rows.append(
            {
                "CourseID": course["id"],
                "Course": course["name"],
                "Department": department or "",
                "Section": section or "",
                "Class Year": course["class_year"],
                "Credits": course["credits"],
                "Instructor": course["instructor"]["name"],
                "Classroom": classroom["name"],
                "Day": item["day"],
                "Start Period": item["start_period"],
                "Num Periods": item["num_periods"],
            }
        )

    st.session_state.schedule_df = pd.DataFrame(rows)


# ----------------- 1단계: CSV 업로드 ----------------- #

st.subheader("1️⃣ 교과목 CSV 업로드")

file = st.file_uploader("CSV 파일 선택 (교과목과 실습실 배정)", type="csv")

if st.button("📤 CSV 업로드"):
    if file is None:
        st.warning("CSV 파일을 선택하세요.")
    else:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/upload_csv/",
                files={"file": (file.name, file.getvalue(), "text/csv")},
            )
        except Exception as e:
            st.error(f"백엔드 연결 오류: {e}")
        else:
            if resp.status_code == 200:
                st.session_state.csv_uploaded = True
                st.session_state.schedule_df = pd.DataFrame()
                st.success("CSV 데이터 업로드 완료!")
            else:
                st.error(f"업로드 오류: {resp.status_code} - {resp.text}")


# ----------------- 2단계: 시간표 생성 ----------------- #

st.subheader("2️⃣ 시간표 생성")

if st.button("🛠 시간표 자동 생성하기"):
    try:
        resp = requests.post(f"{BACKEND_URL}/schedule/generate")
    except Exception as e:
        st.error(f"백엔드 생성 오류: {e}")
    else:
        if resp.status_code == 200:
            st.success("시간표 생성 완료!")
            fetch_schedule_from_backend()
        else:
            st.error(f"생성 오류: {resp.status_code} - {resp.text}")


# ----------------- 3단계: 시간표 조회 ----------------- #

st.subheader("3️⃣ 시간표 조회")

if st.session_state.schedule_df.empty:
    fetch_schedule_from_backend()

schedule_df = st.session_state.schedule_df

if schedule_df.empty:
    st.info("아직 시간표가 없습니다. CSV 업로드 후 생성하세요!")
    st.stop()

# --- 3.1 상세 목록 --- #
st.markdown("### 📋 상세 시간표 목록")
st.dataframe(schedule_df, use_container_width=True, height=300)

# --- 3.2 학년/반 시간표 --- #
st.markdown("### 🗓 학년·반별 시간표 조회")

years = sorted(schedule_df["Class Year"].unique())
selected_year = st.selectbox("학년 선택:", years)

df_year = schedule_df[schedule_df["Class Year"] == selected_year]

if df_year.empty:
    st.warning("해당 학년의 시간표가 없습니다.")
else:

    # ------------------------------
    # 🆕 학과별 필터링
    # ------------------------------
    filter_by_department = st.checkbox("학과별 필터링")

    selected_department = None
    if filter_by_department:
        departments = sorted(
            d for d in df_year["Department"].unique()
            if isinstance(d, str) and d.strip() != ""
        )
        selected_department = st.selectbox("학과 선택:", departments)
        df_year = df_year[df_year["Department"] == selected_department]
        st.caption(f"📌 선택한 학과: **{selected_department}**")

    # ------------------------------
    # 반 선택
    # ------------------------------
    sections = sorted(
        s for s in df_year["Section"].unique()
        if isinstance(s, str) and s.strip() != ""
    )

    df_show = df_year

    if sections:
        selected_section = st.selectbox("반 선택:", sections)
        df_show = df_year[df_year["Section"] == selected_section]

        if selected_department:
            st.caption(f"📌 {selected_department}학과 {selected_section}반 시간표")
        else:
            st.caption(f"📌 {selected_section}반 시간표")

    if df_show.empty:
        st.warning("해당 조건에 맞는 강의가 없습니다.")
    else:
        # ----------------- 시간표 매트릭스 생성 ----------------- #
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        periods = [str(i) for i in range(1, 9)]

        matrix = {day: {p: "" for p in periods} for day in days}

        for _, row in df_show.iterrows():
            day = row["Day"]
            start_p = int(row["Start Period"])
            num_p = int(row["Num Periods"])

            dept = row.get("Department", "").strip()
            section = row["Section"].strip()
            year = str(row["Class Year"])

            # 라벨 구성
            if dept and section:
                class_label = f"{dept} {section}"
            elif section:
                class_label = section
            elif dept:
                class_label = f"{dept} {year}"
            else:
                class_label = year

            text = f"{row['Course']} ({class_label}, {row['Instructor']}, R{row['Classroom']})"

            for p in range(start_p, start_p + num_p):
                key = str(p)
                cell = matrix[day][key]
                if text not in cell.split(" | "):
                    matrix[day][key] = (cell + " | " if cell else "") + text

        # ----------------- 테이블 출력 ----------------- #
        timetable_rows = []
        for p in periods:
            row_data = {"교시": int(p)}
            for d in days:
                row_data[d] = matrix[d][p]
            timetable_rows.append(row_data)

        timetable_df = pd.DataFrame(timetable_rows)
        st.table(timetable_df)
# ----------------- END OF FILE ----------------- #