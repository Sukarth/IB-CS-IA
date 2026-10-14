from datetime import datetime
from .user import User
from .enums import UserRole
from app.database import query

class Admin(User):
    def get_classrooms(self):
        from .classroom import Classroom
        rows = query("SELECT * FROM CLASSROOMS")
        return [Classroom._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['name'], row['email'], row['password_hash'], UserRole(row['role']), bool(row['is_active']), datetime.fromisoformat(row['created_at']))

    

