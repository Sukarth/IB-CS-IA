from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query_one
from datetime import datetime
from .enums import ProgressStatus, UserRole
import math

if TYPE_CHECKING:
    from .student import Student
    from .assignment import Assignment

class ProgressRecord:
    def __init__(self, id: int, student_id: int, assignment_id: int, status: ProgressStatus, status_changed_at: datetime, notes: str, hours_completed: float = 0.0):
        self.id = id
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.status = status
        self.status_changed_at = status_changed_at
        self.notes = notes
        self.hours_completed = hours_completed

    def set_status(self, status: ProgressStatus, notes: str | None = None):
        status = ProgressStatus(status)
        if notes is None:
            notes = self.notes
        execute("UPDATE PROGRESS_RECORDS SET status = ?, status_changed_at = ?, notes = ? WHERE id = ?",
                (status.value, datetime.now().isoformat(), notes, self.id))
        self.status = status
        self.status_changed_at = datetime.now()
        self.notes = notes
        return self

    @classmethod
    def get_or_create(cls, student: Student, assignment: Assignment):
        from .classroom import Classroom
        if student.role != UserRole.STUDENT:
            raise ValueError("Only students can have progress records!")
        
        record = cls.get_progress(student, assignment)
        
        if record: return record

        if student.id not in [s.id for s in Classroom.get_by_id(assignment.classroom_id).get_students()]:
            raise ValueError("Cannot create a progress record for a student who is not enrolled in the classroom containing the assignment.")
        
        execute("INSERT INTO PROGRESS_RECORDS (student_id, assignment_id, status, status_changed_at) VALUES (?, ?, ?, ?)", (student.id, assignment.id, ProgressStatus.NOT_STARTED.value, datetime.now().isoformat()))

        return cls.get_progress(student, assignment)

    @classmethod
    def get_progress(cls, student: Student, assignment: Assignment):
        row = query_one("SELECT * FROM PROGRESS_RECORDS WHERE student_id = ? AND assignment_id = ?", (student.id, assignment.id))
        if not row:
            return None
        
        return cls._from_row(row)

    
    def log_hours(self, hours: float):
        if hours < 0:
            raise ValueError("Hours completed cannot be negative!")
        if not math.isfinite(hours):
            raise ValueError("Hours completed must be a finite number!")
        
        execute("UPDATE PROGRESS_RECORDS SET hours_completed = hours_completed + ? WHERE id = ?", (hours, self.id))
        self.hours_completed += hours
        return self

    @classmethod
    def get_by_id(cls, progress_record_id: int):
        row = query_one("SELECT * FROM PROGRESS_RECORDS WHERE id = ?", (progress_record_id,))
        if not row:
            return None
        
        return cls._from_row(row)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['student_id'], row['assignment_id'], ProgressStatus(row['status']), datetime.fromisoformat(row['status_changed_at']), row['notes'], row['hours_completed'])

    