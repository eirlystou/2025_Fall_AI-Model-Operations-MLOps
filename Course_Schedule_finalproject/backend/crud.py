# backend/crud.py
from typing import List
from sqlalchemy.orm import Session, joinedload

from . import models
from .scheduler.scheduler import ScheduledItem


# ----------- INSTRUCTORS ----------- #

def get_or_create_instructor(db: Session, name: str) -> models.Instructor:
    inst = db.query(models.Instructor).filter_by(name=name).first()
    if inst:
        return inst
    inst = models.Instructor(name=name)
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


# ----------- CLASSROOMS ----------- #

DEFAULT_CLASSROOMS = [
    ("1215", 40),
    ("1216", 40),
    ("1217", 40),
    ("1418", 40),
    ("OTHER", 100),
]


def ensure_default_classrooms(db: Session):
    for name, cap in DEFAULT_CLASSROOMS:
        room = db.query(models.Classroom).filter_by(name=name).first()
        if not room:
            room = models.Classroom(name=name, capacity=cap)
            db.add(room)
    db.commit()


def get_all_classrooms(db: Session) -> List[models.Classroom]:
    return db.query(models.Classroom).all()


# ----------- COURSES ----------- #

def get_all_courses(db: Session) -> List[models.Course]:
    return db.query(models.Course).options(
        joinedload(models.Course.instructor)
    ).all()


def clear_all_data(db: Session):
    db.query(models.Schedule).delete()
    db.query(models.Course).delete()
    db.query(models.Instructor).delete()
    db.commit()


# ----------- SCHEDULE ----------- #

def clear_schedule(db: Session):
    db.query(models.Schedule).delete()
    db.commit()


def save_schedule(db: Session, items: List[ScheduledItem]):
    room_map = {r.name: r.id for r in db.query(models.Classroom).all()}

    for it in items:
        room_id = room_map.get(it.room)
        if room_id is None:
            continue
        s = models.Schedule(
            week=1,
            day=it.day,
            start_period=it.start_period,
            num_periods=it.num_periods,
            course_id=it.course_id,
            classroom_id=room_id,
        )
        db.add(s)
    db.commit()


def get_schedule(db: Session) -> List[models.Schedule]:
    return (
        db.query(models.Schedule)
        .options(
            joinedload(models.Schedule.course).joinedload(models.Course.instructor),
            joinedload(models.Schedule.classroom),
        )
        .order_by(models.Schedule.day, models.Schedule.start_period)
        .all()
    )
