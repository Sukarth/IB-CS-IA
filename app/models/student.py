from app.database import query
from datetime import datetime
from .user import User
from .enums import UserRole

class Student(User):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime, year_group_id: int | None = None):
        super().__init__(id, name, email, password_hash, role, is_active, created_at)
        self.year_group_id = year_group_id
    
    def get_classrooms(self):
        from .classroom import Classroom
        rows = query("SELECT CLASSROOMS.* FROM CLASSROOMS INNER JOIN ENROLLMENTS ON ENROLLMENTS.classroom_id = CLASSROOMS.id WHERE ENROLLMENTS.student_id = ? AND CLASSROOMS.is_published = ?", (self.id, True))
        return [Classroom._from_row(row) for row in rows]
    
    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['name'], row['email'], row['password_hash'], UserRole(row['role']), bool(row['is_active']), datetime.fromisoformat(row['created_at']), row['year_group_id'] if 'year_group_id' in row.keys() else None)
    

