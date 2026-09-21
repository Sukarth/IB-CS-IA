from ..models.assignment import Assignment
from ..models.student import Student
from ..models.enums import UserRole
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
    return assignment.effort_hours * student_settings.procrastination_factor - (0 if ProgressRecord.get_progress(student, assignment) is None else ProgressRecord.get_progress(student, assignment).hours_completed )

def _return_phases(assignment: Assignment):
    queue = Queue()
    for work_chunk in assignment.get_split_effort_hours():
        queue.enqueue(work_chunk)
    return queue

def build_study_schedule(student: Student):
    """Build a study schedule for a student based on the priority of work chunks."""
    if not student or student.role != UserRole.STUDENT:
        raise ValueError("Only students can have a study schedule generated!")

    student_settings = StudentSettings.get_by_student_id(student.id)
    if not student_settings:
        raise ValueError("Student settings not found for the given student!")
    assignments = Assignment.get_for_student(student.id)
    
    if student_settings.exclude_overdue:
        assignments = [a for a in assignments if a.deadline >= datetime.now()]

    phases = {a.id: _return_phases(a) for a in assignments}
    remaining = {a.id: _remaining_effort_hours(a, student, student_settings) for a in assignments}
    plan = {}
    warnings=[]
    
    for offset in range(15):
        day_date = date.today() + timedelta(days=offset)
        free_hours = StudentSettings.get_hours_for_day(student.id, day_date.weekday())
        if free_hours == 0: continue

        pq = PriorityQueue()
        for assignment in assignments:
            if remaining[assignment.id] > 0:
                priority = calculate_assignment_priority(assignment, student, day_date)
                if priority > 0:
                    warnings.append(f"Warning: Assignment '{assignment.name}' has insufficient time to complete before the deadline.")
                pq.enqueue(assignment, priority)

        blocks = []
        while free_hours > 0 and not pq.is_empty():
            assignment = pq.dequeue()
            
            while free_hours > 0 and remaining[assignment.id] > 0:
                chunk = phases[assignment.id].peek()
                used_hours = min(chunk.effort_hours, free_hours)
                blocks.append(ScheduledBlock(assignment.id, chunk.name, used_hours))
                free_hours -= used_hours
                chunk.effort_hours -= used_hours
                if chunk.effort_hours == 0:
                    phases[assignment.id].dequeue()
                
        plan[day_date] = blocks
    
    return StudyPlan(plan, warnings, date.today())
