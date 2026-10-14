from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query, query_one
from datetime import datetime, timedelta
from .enums import UserRole
import secrets, hashlib

if TYPE_CHECKING:
    from .user import User
    from .admin import Admin

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
    
    @classmethod
    def generate(cls, role_to_assign: UserRole, created_by: Admin, valid_days: int, year_group_id: int | None = None):
        from .year_group import YearGroup
        if not created_by or created_by.role != UserRole.ADMIN:
            raise ValueError("Only admins can generate activation keys!")
        if valid_days <= 0:
            raise ValueError("Key validity must be greater than 0 days!")
        if not year_group_id and role_to_assign == UserRole.STUDENT:
            raise ValueError("Year group ID MUST be provided for creating a student activation key!")
        if year_group_id and role_to_assign != UserRole.STUDENT:
            raise ValueError("Year group ID can only be provided for student activation keys!")
        if year_group_id and not YearGroup.get_by_id(year_group_id):
            raise ValueError("Year group does not exist!")
        
        key = secrets.token_hex(4).upper()
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        expires_at = (datetime.now() + timedelta(days=valid_days)).isoformat()
        
        execute("INSERT INTO ACTIVATION_KEYS (key_hash, role_to_assign, created_by_id, created_at, expires_at, is_used, used_by_id, used_at, year_group_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (key_hash, role_to_assign.value, created_by.id, datetime.now().isoformat(), expires_at, False, None, None, year_group_id))
        
        return key
    
    @classmethod
    def generate_batch(cls, role_to_assign: UserRole, created_by: Admin, valid_days: int, count: int, year_group_id: int | None = None):
        if valid_days <= 0:
            raise ValueError("Key validity must be greater than 0 days!")
        if count <= 0:
            raise ValueError("Count must be greater than 0!")
        if not year_group_id and role_to_assign == UserRole.STUDENT:
            raise ValueError("Year group ID MUST be provided for creating student activation keys!")
        if year_group_id and role_to_assign != UserRole.STUDENT:
            raise ValueError("Year group ID can only be provided for student activation keys!")
        
        keys = []
        for _ in range(count):
            key = cls.generate(role_to_assign, created_by, valid_days, year_group_id)
            keys.append(key)
        
        return keys

    @classmethod
    def validate(cls, activation_key: str):
        key_hash = hashlib.sha256(activation_key.strip().encode()).hexdigest()
        row = query_one("SELECT * FROM ACTIVATION_KEYS WHERE key_hash = ? AND is_used = 0 AND expires_at > ?",
                    (key_hash, datetime.now().isoformat()))
        
        return cls._from_row(row) if row else None

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM ACTIVATION_KEYS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls._from_row(row)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['key_hash'], UserRole(row['role_to_assign']), row['created_by_id'], datetime.fromisoformat(row['created_at']), datetime.fromisoformat(row['expires_at']), bool(row['is_used']), row['year_group_id'], row['used_by_id'], datetime.fromisoformat(row['used_at']) if row['used_at'] else None)

    @classmethod
    def get_all(cls):
        rows = query("SELECT * FROM ACTIVATION_KEYS ORDER BY id DESC")
        return [cls._from_row(row) for row in rows]

    def mark_used(self, used_by_user: User):
        if self.is_used:
            raise ValueError("Activation key has already been used!")
        if self.expires_at < datetime.now():
            raise ValueError("Activation key has expired!")
        
        execute("UPDATE ACTIVATION_KEYS SET is_used = 1, used_by_id = ?, used_at = ? WHERE id = ?", (used_by_user.id, datetime.now().isoformat(), self.id))
        self.is_used = True
        self.used_by_id = used_by_user.id
        self.used_at = datetime.now()

        return self

    def delete(self):
        if self.is_used:
            raise ValueError("Cannot delete an activation key that has already been used!")
        execute("DELETE FROM ACTIVATION_KEYS WHERE id = ?", (self.id,))
        return True

    @staticmethod
    def get_count():
        row = query_one("SELECT COUNT(*) as count FROM ACTIVATION_KEYS")
        return row['count'] if row else 0