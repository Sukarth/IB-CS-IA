from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import execute, query, query_one
from datetime import datetime, timedelta
from .enums import UserRole
import bcrypt

if TYPE_CHECKING:
    from .user import User

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
    def generate(cls, role_to_assign: UserRole, created_by: UserRole, valid_days: int, year_group_id: int | None = None):
        if created_by != UserRole.ADMIN:
            raise ValueError("Only admins can generate activation keys!")
        if valid_days <= 0:
            raise ValueError("Key validity must be greater than 0 days!")
        if not year_group_id and role_to_assign == UserRole.STUDENT:
            raise ValueError("Year group ID MUST be provided for creating a student activation key!")
        
        # allow floats for valid_days?
        key = bcrypt.gensalt().decode('utf-8')
        key_hash = bcrypt.hashpw(key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        expires_at = datetime.now().isoformat() + str(timedelta(days=valid_days))
        
        execute("INSERT INTO ACTIVATION_KEYS (key_hash, role_to_assign, created_by_id, created_at, expires_at, is_used, used_by_id, used_at, year_group_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (key_hash, role_to_assign.value, created_by.value, datetime.now().isoformat(), expires_at, False, None, None, year_group_id))
        
        return key
    
    @classmethod
    def generate_batch(cls, role_to_assign: UserRole, created_by: UserRole, valid_days: int, count: int, year_group_id: int | None = None):
        if created_by != UserRole.ADMIN:
            raise ValueError("Only admins can generate activation keys!")
        if valid_days <= 0:
            raise ValueError("Key validity must be greater than 0 days!")
        if count <= 0:
            raise ValueError("Count must be greater than 0!")
        if not year_group_id and role_to_assign == UserRole.STUDENT:
            raise ValueError("Year group ID MUST be provided for creating student activation keys!")
        
        keys = []
        for _ in range(count):
            key = cls.generate(role_to_assign, created_by, valid_days, year_group_id)
            keys.append(key)
        
        return keys

    @classmethod
    def validate(cls, activation_key: str):
        row = query_one("SELECT * FROM ACTIVATION_KEYS WHERE is_used = 0 AND expires_at > ?", (datetime.now().isoformat(),))
        if not row:
            return None
        
        if bcrypt.checkpw(activation_key.encode('utf-8'), row['key_hash'].encode('utf-8')):
            return cls(row['id'], row['key_hash'], UserRole(row['role_to_assign']), row['created_by_id'], datetime.fromisoformat(row['created_at']), datetime.fromisoformat(row['expires_at']), bool(row['is_used']), row['year_group_id'], row['used_by_id'], datetime.fromisoformat(row['used_at']) if row['used_at'] else None)
        
        return None

    def mark_used(self, used_by_user: User):
        if self.is_used:
            raise ValueError("Activation key has already been used!")
        if self.expires_at < datetime.now().isoformat():
            raise ValueError("Activation key has expired!")
        
        execute("UPDATE ACTIVATION_KEYS SET is_used = 1, used_by_id = ?, used_at = ? WHERE id = ?", (used_by_user.id, datetime.now().isoformat(), self.id))
        self.is_used = True
        self.used_by_id = used_by_user.id
        self.used_at = datetime.now().isoformat()

        return self

    def delete(self):
        execute("DELETE FROM ACTIVATION_KEYS WHERE id = ?", (self.id,))
        return True