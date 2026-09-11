from app.database import execute, query, query_one
from datetime import datetime
from .user import User
from .enums import UserRole
from .classroom import Classroom

class Student(User):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime, year_group_id: int | None = None):
        super().__init__(id, name, email, password_hash, role, is_active, created_at)
        self.year_group_id = year_group_id
    
    def get_classrooms(self):
        rows = query("SELECT CLASSROOMS.* FROM CLASSROOMS INNER JOIN ENROLLMENTS ON ENROLLMENTS.classroom_id = CLASSROOMS.id WHERE ENROLLMENTS.student_id = ?", (self.id,))
        return [Classroom._from_row(row) for row in rows]
    

