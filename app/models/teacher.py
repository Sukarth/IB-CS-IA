from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from .user import User
from .enums import UserRole

if TYPE_CHECKING:
    from .classroom import Classroom

class Teacher(User):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime, owned_classrooms: list[Classroom]):
        super().__init__(id, name, email, password_hash, role, is_active, created_at)
        self.owned_classrooms = owned_classrooms
