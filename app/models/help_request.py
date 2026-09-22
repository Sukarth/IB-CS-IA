from datetime import datetime
from app.database import execute, query, query_one
from .enums import UserRole, ProgressStatus
from .assignment import Assignment
from .student import Student
from .progress_record import ProgressRecord
from .classroom import Classroom

class HelpRequest:
    def __init__(self, id: int, student_id: int, assignment_id: int, message: str, created_at: datetime, is_urgent: bool, resolution_notes: str | None = None, resolved_at: datetime | None = None, resolved_by_id: int | None = None):
        self.id = id
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.message = message
        self.created_at = created_at
        self.is_urgent = is_urgent
        self.resolution_notes = resolution_notes
        self.resolved_at = resolved_at
        self.resolved_by_id = resolved_by_id

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['student_id'], row['assignment_id'], row['message'], datetime.fromisoformat(row['created_at']), bool(row['is_urgent']), row['resolution_notes'], datetime.fromisoformat(row['resolved_at']) if row['resolved_at'] else None, row['resolved_by_id'])
    
    @classmethod
    def get_by_id(cls, help_request_id: int):
        row = query_one("SELECT * FROM HELP_REQUESTS WHERE id = ?", (help_request_id,))
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    def create(cls, student: Student, assignment: Assignment, message: str, is_urgent: bool):
        if not student or student.role != UserRole.STUDENT:
            raise ValueError("Only students can create help requests!")
        
        if not query_one("SELECT * FROM ASSIGNMENTS WHERE id = ?", (assignment.id,)):
            raise ValueError("Assignment does not exist.")

        classroom = Classroom.get_by_id(assignment.classroom_id)
        if not classroom:
            raise ValueError("Classroom does not exist.")

        if not classroom.is_published:
            raise ValueError("Cannot create a help request for an unpublished classroom.")

        if not assignment.is_published:
            raise ValueError("Cannot create a help request for an unpublished assignment.")
        
        req = cls.get_by_id(execute("INSERT INTO HELP_REQUESTS (student_id, assignment_id, message, created_at, is_urgent) VALUES (?, ?, ?, ?, ?)", (student.id, assignment.id, message, datetime.now().isoformat(), is_urgent)))
        ProgressRecord.get_or_create(student, assignment).set_status(ProgressStatus.NEEDS_HELP)
        return req

    @classmethod
    def get_unresolved_for_teacher(cls, teacher_id: int):
        rows = query("SELECT HELP_REQUESTS.* FROM HELP_REQUESTS INNER JOIN ASSIGNMENTS ON HELP_REQUESTS.assignment_id = ASSIGNMENTS.id INNER JOIN CLASSROOMS ON ASSIGNMENTS.classroom_id = CLASSROOMS.id WHERE HELP_REQUESTS.resolved_at IS NULL AND CLASSROOMS.teacher_id = ?", (teacher_id,))
        return [HelpRequest._from_row(row) for row in rows]

    def resolve(self, resolved_by_id: int, resolution_notes: str):
        if self.resolved_at is not None:
            raise ValueError("Help request is already resolved.")
        execute("UPDATE HELP_REQUESTS SET resolved_by_id = ?, resolution_notes = ?, resolved_at = ? WHERE id = ?", (resolved_by_id, resolution_notes, datetime.now().isoformat(), self.id))
        student = Student.get_by_id(self.student_id)
        assignment = Assignment.get_by_id(self.assignment_id)
        prog = ProgressRecord.get_or_create(student, assignment)
        if prog.status == ProgressStatus.NEEDS_HELP:
            prog.set_status(ProgressStatus.IN_PROGRESS)
        self.resolution_notes = resolution_notes
        self.resolved_at = datetime.now()
        self.resolved_by_id = resolved_by_id
        
        return self