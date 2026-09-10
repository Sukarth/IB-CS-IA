from datetime import datetime
from .user import User
from .enums import UserRole

class Admin(User):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime):
        super().__init__(id, name, email, password_hash, role, is_active, created_at)
    

