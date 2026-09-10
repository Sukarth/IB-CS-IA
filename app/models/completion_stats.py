from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query, query_one
from datetime import datetime
from .student import Student

if TYPE_CHECKING:
    from .assignment import Assignment

class CompletionStats:
    
    def __init__(self, assignment_id: int, total_students: int, completion_count: int, completion_percentage: float, completed_students: list[Student], pending_students: list[Student], first_submission_at: datetime | None = None, last_submission_at: datetime | None = None):
        self.assignment_id = assignment_id
        self.total_students = total_students
        self.completion_count = completion_count
        self.completion_percentage = completion_percentage
        self.completed_students = completed_students
        self.pending_students = pending_students
        self.first_submission_at = first_submission_at
        self.last_submission_at = last_submission_at

    @classmethod
    def get_by_assignment(cls, assignment: Assignment):
        total_students = query_one("SELECT COUNT(*) as total FROM ENROLLMENTS WHERE classroom_id = ?", (assignment.classroom_id,))
        completion_count = query_one("SELECT COUNT(DISTINCT student_id) as completed FROM SUBMISSIONS WHERE assignment_id = ?", (assignment.id,))
        completion_percentage = (completion_count['completed'] / total_students['total']) * 100 if total_students['total'] > 0 else 0
        
        completed_students_rows = query("SELECT DISTINCT STUDENTS.* FROM STUDENTS INNER JOIN SUBMISSIONS ON STUDENTS.id = SUBMISSIONS.student_id WHERE SUBMISSIONS.assignment_id = ?", (assignment.id,))
        completed_students = [Student._from_row(row) for row in completed_students_rows]
        
        pending_students_rows = query("SELECT * FROM STUDENTS WHERE STUDENTS.id NOT IN (SELECT DISTINCT student_id FROM SUBMISSIONS WHERE assignment_id = ?) AND STUDENTS.id IN (SELECT student_id FROM ENROLLMENTS WHERE classroom_id = ?)", (assignment.id, assignment.classroom_id))
        pending_students = [Student._from_row(row) for row in pending_students_rows]
        
        first_submission_at = query_one("SELECT MIN(submitted_at) as first FROM SUBMISSIONS WHERE assignment_id = ?", (assignment.id,))
        last_submission_at = query_one("SELECT MAX(submitted_at) as last FROM SUBMISSIONS WHERE assignment_id = ?", (assignment.id,))
        
        if first_submission_at:
            first_submission_at = datetime.fromisoformat(first_submission_at['first'])
        if last_submission_at:
            last_submission_at = datetime.fromisoformat(last_submission_at['last'])
        
        return cls(assignment.id, total_students['total'], completion_count['completed'], completion_percentage, completed_students, pending_students, first_submission_at, last_submission_at)