from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query, query_one
from datetime import datetime
from .user import User
from .enums import UserRole
from .classroom import Classroom

class Teacher(User):
    def get_classrooms(self):
        rows = query("SELECT * FROM CLASSROOMS WHERE teacher_id = ?", (self.id,))
        return [Classroom._from_row(row) for row in rows]