import warnings
from ..models.work_chunk import WorkChunk
from ..models.assignment import Assignment
from ..models.student import Student
from ..models.enums import UserRole
from ..models.teacher import Teacher
from ..models.help_request import HelpRequest
from ..adt.priority_queue import PriorityQueue
from ..adt.queue import Queue
from ..models.student_settings import StudentSettings
from datetime import datetime, timedelta
from .assignment_priority import calculate_assignment_priority
from .scheduled_block import ScheduledBlock
from ..models.progress_record import ProgressRecord


def _remaining_effort_hours(assignment: Assignment, student: Student):
    """Calculate the remaining effort hours for an assignment for a student."""
    return assignment.effort_hours * StudentSettings.get_by_student_id(student.id).procrastination_factor - ProgressRecord.get_or_create(student, assignment).hours_completed

def _return_phases(assignment: Assignment):
    queue = Queue()
    for work_chunk in assignment.get_split_effort_hours():
        queue.enqueue(work_chunk)
    return queue

def build_study_schedule(student: Student):
    """Build a study schedule for a student based on the priority of work chunks."""
    student_settings = StudentSettings.get_by_student_id(student.id)
    if not student or student.role != UserRole.STUDENT:
        raise ValueError("Only students can have a study schedule generated!")

    assignments = Assignment.get_for_student(student.id)
    
    if student_settings.exclude_overdue:
        assignments = [a for a in assignments if a.deadline >= datetime.now()]

    today = datetime.now().date().weekday()
    plan = {}
    warnings=[]
    for day in [day % 7 for day in range(today, today + 15)]:
        free_hours = student_settings.get_hours_for_day(day)
        if free_hours == 0: continue

        pq = PriorityQueue()
        [pq.enqueue(assignment, calculate_assignment_priority(assignment, student, day)) for assignment in assignments if _remaining_effort_hours(assignment, student) > 0]

        blocks = []
        while free_hours > 0 and not pq.is_empty():
            assignment = pq.dequeue()
            
            while free_hours > 0 and _remaining_effort_hours(assignment, student) > 0:
                chunk = _return_phases(assignment).peek()
                used_hours = min(chunk.effort_hours, free_hours)
                blocks.append(ScheduledBlock(assignment.id, chunk.name, used_hours))
                free_hours -= used_hours
                chunk.effort_hours -= used_hours
                if chunk.effort_hours == 0:
                    _return_phases(assignment).dequeue()
        plan[datetime.now().date() + timedelta(days=day)] = blocks        
