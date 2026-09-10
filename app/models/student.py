from datetime import datetime
from .user import User
from .enums import UserRole

class Student(User):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime, year_group_id: int | None = None):
        super().__init__(id, name, email, password_hash, role, is_active, created_at)
        self.year_group_id = year_group_id
    

