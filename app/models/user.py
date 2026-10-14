from app.database import execute, query, query_one
from datetime import datetime
from .enums import UserRole
from .activation_key import ActivationKey
from .student_settings import StudentSettings
from abc import ABC, abstractmethod
from email_validator import validate_email, EmailNotValidError
import bcrypt
import re

class User(ABC):
    def __init__(self, id: int, name: str, email: str, password_hash: str, role: UserRole, is_active: bool, created_at: datetime):
        self.id = id
        self.name = name
        self.email = email.strip().lower()
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

    @staticmethod
    def _validate_email(email: str):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False


    @staticmethod
    def _validate_password(password: str):
        if len(password) < 8:
            return (False, "Password must be at least 8 characters long")
        elif re.search('[0-9]', password) is None:
            return (False, "Password must contain at least one number")
        elif re.search('[A-Z]', password) is None:
            return (False, "Password must contain at least one uppercase letter")
        elif re.search('[a-z]', password) is None:
            return (False, "Password must contain at least one lowercase letter")
        elif re.search('[!@#$%^&*(),.?":{}|<>]', password) is None:
            return (False, "Password must contain at least one special character")
        return (True, "Password is valid")


    @classmethod
    def register(cls, name: str, email: str, password: str, activation_key: str):
        name = name.strip()
        if not name:
            raise ValueError('Name cannot be blank!')
        if not email:
            raise ValueError('Email cannot be blank!')
        email = email.strip().lower()
        if not cls._validate_email(email):
            raise ValueError('Invalid email address!')
        if not password:
            raise ValueError('Password cannot be blank!')
        if not activation_key:
            raise ValueError('Activation key cannot be blank!')
        
        if cls.get_by_email(email):
            raise ValueError("Email is already in use!")
        activation = ActivationKey.validate(activation_key)
        if not activation:
            raise ValueError("Invalid activation key!")
        
        is_valid, message = cls._validate_password(password)
        if not is_valid:
            raise ValueError(message)

        password_hash = cls._hash_password(password)
        
        user_id = execute("INSERT INTO USERS (name, email, password_hash, role, is_active, created_at, year_group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, email, password_hash, activation.role_to_assign.value, True, datetime.now().isoformat(), activation.year_group_id))

        if activation.role_to_assign == UserRole.STUDENT:
            StudentSettings.create(user_id)
            
        user = cls.get_by_id(user_id)
        activation.mark_used(user)
        
        return user

    @classmethod
    def _from_row(cls, row):
        from .admin import Admin
        from .student import Student
        from .teacher import Teacher
        user_typer = {UserRole.ADMIN: Admin, UserRole.STUDENT: Student, UserRole.TEACHER: Teacher}
        return user_typer[UserRole(row['role'])]._from_row(row)

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM USERS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls._from_row(row)

    @classmethod
    def get_by_email(cls, email: str):
        row = query_one("SELECT * FROM USERS WHERE email = ?", (email.strip().lower(),))
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
        email = email.strip().lower()
        if not email:
            raise ValueError('Email cannot be blank!')
        if not password:
            raise ValueError('Password cannot be blank!')
        if not cls._validate_email(email):
            raise ValueError('Invalid email address!')
        user = cls.get_by_email(email)
        
        if not user or not cls._check_password(password, user.password_hash):
            raise ValueError('Invalid email or password!')

        if not user.is_active:
            raise ValueError('Account not active (is disabled)!')
        
        return user

    def update_profile(self, name: str, email: str):
        name = name.strip()
        email = email.strip().lower()
        if not email:
            raise ValueError('Email is required!')
        if not name:
            raise ValueError('Name is required!')
        if not self._validate_email(email):
            raise ValueError('Invalid email address!')
        
        existing_user = self.get_by_email(email)
        if existing_user and existing_user.id != self.id:
            raise ValueError('Email is already in use!')

        execute("UPDATE USERS SET name = ?, email = ? WHERE id = ?", (name, email, self.id))

        self.name = name
        self.email = email

        return self

    def change_password(self, current_password: str, new_password: str):
        if not current_password:
            raise ValueError('Current password is required!')
        if not new_password:
            raise ValueError('New password is required!')
        if not self._check_password(current_password, self.password_hash):
            raise ValueError('Incorrect current password!')

        is_valid, message = self._validate_password(new_password)
        if not is_valid:
            raise ValueError(message)
        
        new_password_hash = self._hash_password(new_password)
        
        execute("UPDATE USERS SET password_hash = ? WHERE id = ?", (new_password_hash, self.id))
        self.password_hash = new_password_hash

        return self

    @classmethod
    def get_all(cls, role=None, year_group_id=None, activated=None):
        query_str = "SELECT * FROM USERS WHERE 6 = 6"
        params = []

        if role is not UserRole.STUDENT and year_group_id:
            raise ValueError("Year group ID can only be specified for students!")

        if role is not None:
            query_str += " AND role = ?"
            params.append(role)

        if year_group_id is not None:
            query_str += " AND year_group_id = ?"
            params.append(year_group_id)
        
        if activated is not None:
            query_str += " AND is_active = ?"
            params.append(activated)

        query_str += " ORDER BY name"

        return [cls._from_row(row) for row in query(query_str, tuple(params))]

    @abstractmethod
    def get_classrooms(self):
        ...

    def deactivate(self):
        if not self.is_active:
            raise ValueError('Account is already deactivated!')
        execute("UPDATE USERS SET is_active = ? WHERE id = ?", (False, self.id))
        self.is_active = False
        
        return self

    def activate(self):
        if self.is_active:
            raise ValueError('Account is already active!')
        execute("UPDATE USERS SET is_active = ? WHERE id = ?", (True, self.id))
        self.is_active = True
        
        return self