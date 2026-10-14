from __future__ import annotations
from typing import TYPE_CHECKING
from .assignment import Assignment
from datetime import datetime
from .material import Material
from app.database import execute, query, query_one
from .enums import UserRole

if TYPE_CHECKING:
    from .student import Student
    from .teacher import Teacher

class Classroom:
    def __init__(self, id: int, name: str, description: str, teacher_id: int, is_published: bool):
        self.id = id
        self.name = name
        self.description = description
        self.teacher_id = teacher_id
        self.is_published = is_published

    @classmethod
    def get_by_id(cls, classroom_id: int):
        row = query_one("SELECT * FROM CLASSROOMS WHERE id = ?", (classroom_id,))
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['name'], row['description'], row['teacher_id'], bool(row['is_published']))

    @classmethod
    def create(cls, name: str, description: str, teacher: Teacher, is_published: bool):
        name = name.strip()
        if teacher.role != UserRole.TEACHER:
            raise ValueError("Only teachers can create classrooms!")
        if not name:
            raise ValueError("Classroom name cannot be blank!")

        classroom_id = execute(
            "INSERT INTO CLASSROOMS (name, description, teacher_id, is_published, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, description, teacher.id, is_published, datetime.now().isoformat())
        )
        return cls.get_by_id(classroom_id)

    def update(self, name: str, description: str):
        name = name.strip()
        if not name:
            raise ValueError("Classroom name cannot be blank!")

        execute(
            "UPDATE CLASSROOMS SET name = ?, description = ? WHERE id = ?",
            (name, description, self.id)
        )
        self.name = name
        self.description = description
        return self

    def delete(self):
        if self.get_assignments():
            raise ValueError("Cannot delete a classroom with assignments. Please remove assignments first.")
        if self.get_materials():
            raise ValueError("Cannot delete a classroom with materials. Please remove materials first.")
        if self.get_students():
            raise ValueError("Cannot delete a classroom with enrolled students. Please unenroll students first.")
        if self.get_help_requests(unresolved_only=False):
            raise ValueError("Cannot delete a classroom with help requests. Please resolve or remove help requests first.")
        execute("DELETE FROM CLASSROOMS WHERE id = ?", (self.id,))
        return True

    def publish(self):
        if self.is_published:
            raise ValueError("Classroom is already published!")
        execute("UPDATE CLASSROOMS SET is_published = ? WHERE id = ?", (True, self.id))
        self.is_published = True
        return self

    def unpublish(self):
        if not self.is_published:
            raise ValueError("Classroom is already unpublished!")
        execute("UPDATE CLASSROOMS SET is_published = ? WHERE id = ?", (False, self.id))
        self.is_published = False
        return self

    def enroll_student(self, student: Student):
        if not student.role == UserRole.STUDENT:
            raise ValueError("Only students can be enrolled in classrooms!")
        if student.id in [s.id for s in self.get_students()]:
            raise ValueError("Student is already enrolled in this classroom!")
        if not student.is_active:
            raise ValueError("Cannot enroll a deactivated student to a classroom!")

        execute("INSERT INTO ENROLLMENTS (classroom_id, student_id, joined_at) VALUES (?, ?, ?)", (self.id, student.id, datetime.now().isoformat()))
        return self
    
    def unenroll_student(self, student: Student):
        if not student.role == UserRole.STUDENT:
            raise ValueError("Only students can be unenrolled from classrooms!")
        if student.id not in [s.id for s in self.get_students()]:
            raise ValueError("Student is not enrolled in this classroom!")

        execute("DELETE FROM ENROLLMENTS WHERE classroom_id = ? AND student_id = ?", (self.id, student.id))
        return self

    def get_assignments(self, published_only: bool = False, unpublished_only: bool = False):
        if published_only:
            rows = query("SELECT * FROM ASSIGNMENTS WHERE classroom_id = ? AND is_published = ?", (self.id, True))
        elif unpublished_only:
            rows = query("SELECT * FROM ASSIGNMENTS WHERE classroom_id = ? AND is_published = ?", (self.id, False))
        else:
            rows = query("SELECT * FROM ASSIGNMENTS WHERE classroom_id = ?", (self.id,))
        return [Assignment._from_row(row) for row in rows]
    
    def get_materials(self):
        rows = query("SELECT * FROM MATERIALS WHERE classroom_id = ?", (self.id,))
        return [Material._from_row(row) for row in rows]

    def get_students(self):
        from .student import Student
        rows = query("SELECT USERS.* FROM USERS INNER JOIN ENROLLMENTS ON USERS.id = ENROLLMENTS.student_id WHERE ENROLLMENTS.classroom_id = ?", (self.id,))
        return [Student._from_row(row) for row in rows]

    def get_help_requests(self, unresolved_only: bool = True):
        from .help_request import HelpRequest
        if unresolved_only:
            rows = query("SELECT HELP_REQUESTS.* FROM HELP_REQUESTS INNER JOIN ASSIGNMENTS ON HELP_REQUESTS.assignment_id = ASSIGNMENTS.id WHERE ASSIGNMENTS.classroom_id = ? AND HELP_REQUESTS.resolved_at IS NULL", (self.id,))
        else:
            rows = query("SELECT HELP_REQUESTS.* FROM HELP_REQUESTS INNER JOIN ASSIGNMENTS ON HELP_REQUESTS.assignment_id = ASSIGNMENTS.id WHERE ASSIGNMENTS.classroom_id = ?", (self.id,))
        return [HelpRequest._from_row(row) for row in rows]