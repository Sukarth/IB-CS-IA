from ..models.assignment import Assignment
from ..models.student import Student
from ..models.enums import UserRole, WarningType
from ..adt.priority_queue import PriorityQueue
from ..adt.queue import Queue
from ..models.student_settings import StudentSettings
from datetime import datetime, timedelta, date
from .assignment_priority import calculate_assignment_priority
from .scheduled_block import ScheduledBlock
from ..models.progress_record import ProgressRecord
from .study_plan import StudyPlan


def _remaining_effort_hours(assignment: Assignment, student: Student, student_settings: StudentSettings):
    """Calculate the remaining effort hours for an assignment for a student."""
    prog_rec = ProgressRecord.get_progress(student, assignment)
    return assignment.effort_hours * student_settings.procrastination_factor - (0 if prog_rec is None else prog_rec.hours_completed)

def _return_phases(assignment: Assignment, student: Student, procrastination_factor: float):
    record = ProgressRecord.get_progress(student, assignment)
    hours_completed = record.hours_completed if record else 0
    queue = Queue()
    for work_chunk in assignment.get_split_effort_hours():
        work_chunk.effort_hours = work_chunk.effort_hours * procrastination_factor
        if hours_completed >= work_chunk.effort_hours:
            hours_completed -= work_chunk.effort_hours
            continue
        work_chunk.effort_hours -= hours_completed
        hours_completed = 0
        queue.enqueue(work_chunk)
    return queue

def build_study_schedule(student: Student, HORIZON_DAYS: int = 14):
    """Build a study schedule for a student based on the priority of work chunks."""
    if not student or student.role != UserRole.STUDENT:
        raise ValueError("Only students can have a study schedule generated!")

    student_settings = StudentSettings.get_by_student_id(student.id)
    if not student_settings:
        raise ValueError("Student settings not found for the given student!")
    assignments = Assignment.get_for_student(student.id)
    
    if student_settings.exclude_overdue:
        assignments = [a for a in assignments if a.deadline >= datetime.now()]

    phases = {a.id: _return_phases(a, student, student_settings.procrastination_factor) for a in assignments}
    remaining = {a.id: _remaining_effort_hours(a, student, student_settings) for a in assignments}
    plan = {}
    warnings=[]

    horizon_end = date.today() + timedelta(days=HORIZON_DAYS)
    
    for offset in range(HORIZON_DAYS + 1):
        day_date = date.today() + timedelta(days=offset)
        plan[day_date] = []
        free_hours = student_settings.get_hours_for_day(day_date.weekday())
        if free_hours == 0: continue

        pq = PriorityQueue()
        for assignment in assignments:
            before_deadline = day_date <= assignment.deadline.date()
            is_overdue = assignment.deadline < datetime.now()
            if remaining[assignment.id] > 1e-9 and (before_deadline or is_overdue):
                priority = calculate_assignment_priority(assignment, student_settings, day_date, remaining[assignment.id])
                pq.enqueue(assignment, priority)

        blocks = []
        while free_hours > 1e-9 and not pq.is_empty():
            assignment = pq.dequeue()
            
            while free_hours > 1e-9 and remaining[assignment.id] > 1e-9 and not phases[assignment.id].is_empty():
                chunk = phases[assignment.id].peek()
                used_hours = min(chunk.effort_hours, free_hours, remaining[assignment.id])
                blocks.append(ScheduledBlock(assignment.id, chunk.name, used_hours))
                free_hours -= used_hours
                chunk.effort_hours -= used_hours
                remaining[assignment.id] -= used_hours
                if chunk.effort_hours <= 1e-9:
                    phases[assignment.id].dequeue()

        plan[day_date] = blocks

    for assignment in assignments:
        if assignment.deadline < datetime.now():
            hours_left = _remaining_effort_hours(assignment, student, student_settings)

            if hours_left <= 1e-9:
                warnings.append((assignment.id, WarningType.OVERDUE, f"'{assignment.title}' is overdue, but can be submitted (you have logged all its hours)."))
            elif remaining[assignment.id] > 1e-9:
                warnings.append((assignment.id, WarningType.OVERDUE, f"'{assignment.title}' is overdue. {remaining[assignment.id]:.1f} hours did not fit into the schedule."))
            else:
                warnings.append((assignment.id, WarningType.OVERDUE, f"'{assignment.title}' is overdue. It has been scheduled as soon as possible."))
        elif remaining[assignment.id] > 1e-9 and assignment.deadline.date() <= horizon_end:
            warnings.append((assignment.id, WarningType.CANNOT_FINISH, f"'{assignment.title}' cannot be finished before its deadline with your current free hours. {remaining[assignment.id]:.1f} hours could not be scheduled."))
    return StudyPlan(plan, warnings, date.today())
