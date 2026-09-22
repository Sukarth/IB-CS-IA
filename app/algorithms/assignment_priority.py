from datetime import date, timedelta
from ..models.assignment import Assignment
from ..models.student_settings import StudentSettings

def calculate_assignment_priority(assignment: Assignment, student_settings: StudentSettings, day_date: date, remaining_hours: float):
    """Calculate the priority of an assignment for a student based on the time remaining until the deadline and the student's settings' available weekday hours."""
    
    student_hours = [student_settings.hours_free_monday, student_settings.hours_free_tuesday, student_settings.hours_free_wednesday, student_settings.hours_free_thursday, student_settings.hours_free_friday, student_settings.hours_free_saturday, student_settings.hours_free_sunday]
    
    days_remaining = (assignment.deadline.date() - day_date).days

    hours_available = sum(student_hours[(day_date + timedelta(days=i)).weekday()] for i in range(days_remaining + 1))

    return remaining_hours - hours_available