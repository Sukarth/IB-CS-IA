from ..models.work_chunk import WorkChunk
from ..models.assignment import Assignment
from ..models.student import Student
from ..models.enums import UserRole
from ..models.teacher import Teacher
from ..models.help_request import HelpRequest
from ..adt.priority_queue import PriorityQueue
from ..adt.queue import Queue
from ..models.student_settings import StudentSettings
from datetime import datetime
from .assignment_priority import calculate_assignment_priority
from .scheduled_block import ScheduledBlock

def build_study_schedule(student: Student):
    """Build a study schedule for a student based on the priority of work chunks."""
    if not student or student.role != UserRole.STUDENT:
        raise ValueError("Only students can have a study schedule generated!")

    assignments = Assignment.get_for_student(student.id)
    
    if StudentSettings.get_by_student_id(student.id).exclude_overdue:
        assignments = [a for a in assignments if a.deadline >= datetime.now()]

    prioritized_assignments = PriorityQueue()
    for assignment in assignments:
        priority = calculate_assignment_priority(assignment, student)
        prioritized_assignments.enqueue(assignment, priority)

    study_schedule = Queue()
    while not prioritized_assignments.is_empty():
        assignment = prioritized_assignments.dequeue()
        for work_chunk in assignment.get_split_effort_hours():
            study_schedule.enqueue(ScheduledBlock(assignment.id, work_chunk.name, work_chunk.hours))

    return study_schedule