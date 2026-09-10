from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query, query_one
from datetime import datetime
from .enums import ProgressStatus

if TYPE_CHECKING:
    from .student import Student
    from .assignment import Assignment

class ProgressRecord:
    def __init__(self, id: int, student_id: int, assignment_id: int, status: ProgressStatus, status_changed_at: datetime, notes: str):
        self.id = id
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.status = status
        self.status_changed_at = status_changed_at
        self.notes = notes

    def set_status(self, student: Student, assignment: Assignment, status: ProgressStatus, notes: str):
        execute("INSERT OR REPLACE INTO PROGRESS_RECORDS (student_id, assignment_id, status, status_changed_at, notes) VALUES (?, ?, ?, ?, ?)", (student.id, assignment.id, status, datetime.now(), notes))
        return self.__class__.get_progress(student, assignment)

    @classmethod
    def get_progress(cls, student: Student, assignment: Assignment):
        row = query_one("SELECT * FROM PROGRESS_RECORDS WHERE student_id = ? AND assignment_id = ?", (student.id, assignment.id))
        if not row:
            return None
        
        return cls(row['id'], row['student_id'], row['assignment_id'], ProgressStatus(row['status']), datetime.fromisoformat(row['status_changed_at']), row['notes'])