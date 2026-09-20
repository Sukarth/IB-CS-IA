from datetime import datetime, date, timedelta
from ..models.assignment import Assignment
from ..models.student import Student
from ..models.student_settings import StudentSettings
from ..models.progress_record import ProgressRecord

def calculate_assignment_priority(assignment: Assignment, student: Student):
    """Calculate the priority of an assignment for a student based on the time remaining until the deadline and the student's settings' available weekday hours."""
    student_settings = StudentSettings.get_by_student_id(student.id)
    
    student_hours = [student_settings.hours_free_monday, student_settings.hours_free_tuesday, student_settings.hours_free_wednesday, student_settings.hours_free_thursday, student_settings.hours_free_friday, student_settings.hours_free_saturday, student_settings.hours_free_sunday]
    
    days_remaining = (assignment.deadline.date() - datetime.now().date()).days

    if days_remaining < 0:
        return 0.0  # Assignment is overdue, no priority
    
    hours_available = sum(student_hours[(datetime.now().date() + timedelta(days=i)).weekday()] for i in range(days_remaining + 1))

    return hours_available - (assignment.effort_hours - ProgressRecord.get_or_create(student, assignment).hours_completed)