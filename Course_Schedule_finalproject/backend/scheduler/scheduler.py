# backend/scheduler/scheduler.py
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ---------------------- DATA MODELS ---------------------- #

@dataclass
class Course:
    id: int
    name: str
    credits: int
    num_weeks: int
    students: int
    instructor: str
    class_year: int
    section: str | None = None
    department: str | None = None


@dataclass
class Classroom:
    name: str
    capacity: int


@dataclass
class ScheduledItem:
    course_id: int
    course_name: str
    class_year: int
    section: str | None
    week: int
    day: str
    start_period: int
    num_periods: int
    room: str
    instructor: str


# ---------------------- CONSTANTS ---------------------- #

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
MAX_PERIODS_PER_DAY = 8


# ---------------------- SPLIT PERIODS ---------------------- #

def split_periods_by_day(credits: int, num_weeks: int) -> List[int]:
    """
    Return the list of periods-per-day for this course.
    - Total = credits * week_multiplier
    - Must be multiples of credits
    - Max 2 days
    """
    periods = credits * (2 if num_weeks == 7 else 1)
    C = credits
    candidates: List[List[int]] = []

    # 1 day option
    if periods % C == 0 and periods <= MAX_PERIODS_PER_DAY:
        candidates.append([periods])

    # 2 day option
    for p1 in range(C, periods, C):
        p2 = periods - p1
        if p2 >= C and p2 % C == 0 and max(p1, p2) <= MAX_PERIODS_PER_DAY:
            candidates.append([p1, p2])

    # fallback
    if not candidates:
        if periods <= MAX_PERIODS_PER_DAY:
            return [periods]
        else:
            return [periods // 2, periods - periods // 2]

    # prefer fewer days, then more balanced split
    candidates.sort(key=lambda x: (len(x), abs(x[0] - (x[1] if len(x) > 1 else 0))))
    return candidates[0]


# ---------------------- CORE ALGORITHM ---------------------- #

def generate_schedule(courses: List[Course], rooms: List[Classroom]) -> List[ScheduledItem]:
    """
    Generate schedule for WEEK 1 – sample for the whole semester.
    Ensures:
      - no room conflict
      - no teacher conflict
      - no class conflict (correctly distinguishes classes by department)
    """
    schedule: List[ScheduledItem] = []

    # room_used[room][day][period]
    room_used: Dict[str, Dict[str, List[bool]]] = {
        r.name: {d: [False] * (MAX_PERIODS_PER_DAY + 1) for d in DAYS}
        for r in rooms
    }

    # teacher_used[teacher][day][period]
    teacher_used: Dict[str, Dict[str, List[bool]]] = {}

    # class_used[(class_year, section, department)][day][period]
    # FIX: add department to distinguish real classes
    class_used: Dict[Tuple[int, str | None, str | None], Dict[str, List[bool]]] = {}

    # sort: difficult courses (big credits, many students) first
    courses_sorted = sorted(
        courses,
        key=lambda c: (-c.credits, -c.students)
    )

    for c in courses_sorted:

        if c.instructor not in teacher_used:
            teacher_used[c.instructor] = {
                d: [False] * (MAX_PERIODS_PER_DAY + 1) for d in DAYS
            }

        # FIX: use department to differentiate classes with same year & section
        class_key = (c.class_year, c.section, c.department)

        if class_key not in class_used:
            class_used[class_key] = {
                d: [False] * (MAX_PERIODS_PER_DAY + 1) for d in DAYS
            }

        per_day_list = split_periods_by_day(c.credits, c.num_weeks)
        days_needed = len(per_day_list)
        day_index = 0

        for day in DAYS:
            if day_index >= days_needed:
                break

            needed = per_day_list[day_index]
            placed = False

            for room in rooms:
                if room.capacity < c.students:
                    continue

                # try all valid start periods
                for start_p in range(1, MAX_PERIODS_PER_DAY - needed + 2):

                    # room conflict
                    if any(room_used[room.name][day][p] for p in range(start_p, start_p + needed)):
                        continue

                    # teacher conflict
                    if any(teacher_used[c.instructor][day][p] for p in range(start_p, start_p + needed)):
                        continue

                    # class conflict (for same department only)
                    if any(class_used[class_key][day][p] for p in range(start_p, start_p + needed)):
                        continue

                    # place course
                    for p in range(start_p, start_p + needed):
                        room_used[room.name][day][p] = True
                        teacher_used[c.instructor][day][p] = True
                        class_used[class_key][day][p] = True

                    schedule.append(
                        ScheduledItem(
                            course_id=c.id,
                            course_name=c.name,
                            class_year=c.class_year,
                            section=c.section,
                            week=1,
                            day=day,
                            start_period=start_p,
                            num_periods=needed,
                            room=room.name,
                            instructor=c.instructor,
                        )
                    )

                    placed = True
                    break  # stop trying start periods

                if placed:
                    break  # stop trying rooms

            if placed:
                day_index += 1

        # (No debug here — skip silently if not placed fully)

    return schedule
