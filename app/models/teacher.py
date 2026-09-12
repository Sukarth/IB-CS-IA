from app.database import execute, query, query_one
from datetime import datetime
from .user import User
from .enums import UserRole
from .classroom import Classroom

class Teacher(User):
    def get_classrooms(self):
        rows = query("SELECT * FROM CLASSROOMS WHERE teacher_id = ?", (self.id,))
        return [Classroom._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['name'], row['email'], row['password_hash'], UserRole(row['role']), bool(row['is_active']), datetime.fromisoformat(row['created_at']))