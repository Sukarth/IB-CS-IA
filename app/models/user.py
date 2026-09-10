from app.database import execute, query, query_one
from datetime import datetime
from .enums import UserRole
from .activation_key import ActivationKey
import bcrypt

class User:
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

    # add a validate email method?

    @classmethod
    def register(cls, name: str, email: str, password: str, activation_key: str):
        if not name:
            raise ValueError('name cannot be blank')
        if not email:
            raise ValueError('email cannot be blank')
        if not password:
            raise ValueError('password cannot be blank')
        if not activation_key:
            raise ValueError('activation key cannot be blank')
        
        row = query_one("SELECT * FROM USERS WHERE email = ?", (email,))
        if row:
            raise ValueError("Email already exists")
        activation = ActivationKey.validate(activation_key)
        if not activation:
            raise ValueError("Invalid activation key")

        password_hash = cls._hash_password(password)
        
        user_id = execute("INSERT INTO USERS (name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (name, email, password_hash, activation.role.value, True, datetime.now().isoformat()))
        return cls.get_by_id(user_id)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['name'], row['email'], row['password_hash'], UserRole(row['role']), bool(row['is_active']), datetime.fromisoformat(row['created_at']))

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM USERS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls._from_row(row)

    @classmethod
    def get_by_email(cls, email: str):
        row = query_one("SELECT * FROM USERS WHERE email = ?", (email,))
        if not row:
            return None
        
        return cls._from_row(row)

    @staticmethod
    def _hash_password(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _check_password(password: str, password_hash: str):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @classmethod
    def authenticate(cls, email: str, password: str):
        if not email:
            raise ValueError('email cannot be blank')
        if not password:
            raise ValueError('password cannot be blank')
        user = cls.get_by_email(email)
        
        if not user or not cls._check_password(password, user.password_hash):
            raise ValueError('invalid email or password')

        if not user.is_active:
            raise ValueError('account not active')
        
        return user

    def update_profile(self, name: str, email: str):
        if not email:
            raise ValueError('email is required')
        if not name:
            raise ValueError('name is required')

        execute("UPDATE USERS SET name = ?, email = ? WHERE id = ?", (name, email, self.id))

        self.name = name
        self.email = email

        return self

    def change_password(self, current_password: str, new_password: str):
        if not current_password:
            raise ValueError('current password is required')
        if not new_password:
            raise ValueError('new password is required')
        # password complexity or length checks?
        if not self._check_password(current_password, self.password_hash):
            raise ValueError('incorrect current password')
        
        new_password_hash = self._hash_password(new_password)
        
        execute("UPDATE USERS SET password_hash = ? WHERE id = ?", (new_password_hash, self.id))
        self.password_hash = new_password_hash

        return self

    def deactivate(self):
        # need to check if user has rights to perform this action? 
        execute("UPDATE USERS SET is_active = ? WHERE id = ?", (False, self.id))
        self.is_active = False
        
        return self