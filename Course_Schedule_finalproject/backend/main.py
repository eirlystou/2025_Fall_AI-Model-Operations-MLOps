# backend/main.py
from collections import defaultdict
from io import StringIO
from typing import List
import csv
import logging

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from .database import init_db, get_db
from . import crud, models, schemas
from .scheduler.scheduler import (
    Course as SCourse,
    Classroom as SClassroom,
    generate_schedule,
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="강의 시간표 및 강의실 자동 배정 시스템")

# 서버 시작 시 DB 초기화
init_db()


# --------------------------------------------------------------------
#  HEALTH CHECK
# --------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "서버 정상 작동 중"}


# --------------------------------------------------------------------
#  COURSES & CLASSROOMS
# --------------------------------------------------------------------
@app.get("/courses", response_model=List[schemas.CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)


@app.get("/classrooms", response_model=List[schemas.ClassroomRead])
def list_classrooms(db: Session = Depends(get_db)):
    crud.ensure_default_classrooms(db)
    return crud.get_all_classrooms(db)


# --------------------------------------------------------------------
#  GENERATE SCHEDULE
# --------------------------------------------------------------------
@app.post("/schedule/generate", response_model=List[schemas.ScheduleRead])
def generate_schedule_endpoint(db: Session = Depends(get_db)):
    crud.ensure_default_classrooms(db)

    courses = crud.get_all_courses(db)
    rooms = crud.get_all_classrooms(db)

    # Scheduler용 모델 변환
    s_courses = [
        SCourse(
            id=c.id,
            name=c.name,
            credits=c.credits,
            num_weeks=c.num_weeks,
            students=c.students,
            instructor=c.instructor.name,
            class_year=c.class_year,
            department=c.department,
            section=c.section,
        )
        for c in courses
    ]

    s_rooms = [SClassroom(name=r.name, capacity=r.capacity) for r in rooms]

    # 시간표 생성
    items = generate_schedule(s_courses, s_rooms)

    # 기존 시간표 삭제 후 새로 저장
    crud.clear_schedule(db)
    crud.save_schedule(db, items)

    return crud.get_schedule(db)


@app.get("/schedule", response_model=List[schemas.ScheduleRead])
def list_schedule(db: Session = Depends(get_db)):
    return crud.get_schedule(db)


# --------------------------------------------------------------------
#  UPLOAD CSV & IMPORT COURSES
# --------------------------------------------------------------------
@app.post("/upload_csv/")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    CSV 파일을 업로드하여 전체 데이터를 초기화 후 재등록:
    - 교수
    - 교과목 (교과목코드, 학년, 분반(예: 3A, 3B...))
    """
    try:
        # 기존 데이터 삭제
        if hasattr(crud, "clear_all_data"):
            crud.clear_all_data(db)
        else:
            # fallback
            db.query(models.Schedule).delete()
            db.query(models.Course).delete()
            db.query(models.Instructor).delete()
            db.commit()

        crud.ensure_default_classrooms(db)

        contents = await file.read()
        try:
            data = StringIO(contents.decode("utf-8"))
        except UnicodeDecodeError:
            data = StringIO(contents.decode("utf-8-sig"))

        csv_reader = csv.DictReader(data)

        # (개설학과, 학년, 교과목코드) 조합별 분반 생성
        section_counter = defaultdict(int)

        for row in csv_reader:
            try:
                instructor_name = row["강좌담당교수"].strip()
                course_name = row["교과목명"].strip()
                course_code = row["교과목코드"].strip()
                department = row["개설학과"].strip()
                credits = int(row["교과목학점"])
                num_weeks = int(row["수업주수"])
                students = int(row["수강인원"])
                class_year = int(row["개설학년"])
            except KeyError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"CSV 파일에 필요한 열이 없습니다: {e}",
                ) from e

            # 분반 생성: 3A, 3B, 3C...
            key = (department, class_year, course_code)
            idx = section_counter[key]
            section_counter[key] += 1

            suffix = chr(ord("A") + idx)
            section = f"{class_year}{suffix}"

            # 교수 정보 생성/조회
            instructor = crud.get_or_create_instructor(db, instructor_name)

            # 교과목 생성
            course = models.Course(
                name=course_name,
                course_code=course_code,
                department=department,
                credits=credits,
                num_weeks=num_weeks,
                students=students,
                class_year=class_year,
                section=section,
                instructor_id=instructor.id,
            )
            db.add(course)

        db.commit()
        return {"message": "CSV 데이터가 성공적으로 업로드되었습니다."}

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("CSV 업로드 처리 중 오류 발생")
        raise HTTPException(status_code=500, detail=f"서버 오류: {e}")
