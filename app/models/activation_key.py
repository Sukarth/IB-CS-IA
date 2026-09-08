from app.database import execute, query, query_one
from datetime import datetime
from .enums import UserRole
import bcrypt

class ActivationKey:
    def __init__(self, id: int, key_hash: str, role_to_assign: UserRole, created_by_id: int, created_at: datetime, expires_at: datetime, is_used: bool, year_group_id: int | None = None, used_by_id: int | None = None, used_at: datetime | None = None):
        self.id = id
        self.key_hash = key_hash
        self.role_to_assign = role_to_assign
        self.created_by_id = created_by_id
        self.created_at = created_at
        self.expires_at = expires_at
        self.is_used = is_used
        self.year_group_id = year_group_id
        self.used_by_id = used_by_id
        self.used_at = used_at
        