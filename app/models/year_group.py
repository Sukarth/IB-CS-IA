from app.database import execute, query, query_one
from datetime import datetime
from .enums import UserRole
from .user import User
from .student import Student

class YearGroup:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name: str):
        if not name:
            raise ValueError("Year group name cannot be blank!")
        if query_one("SELECT * FROM YEAR_GROUPS WHERE name = ?", (name,)):
            raise ValueError("Year group name already exists!")
        
        year_group_id = execute("INSERT INTO YEAR_GROUPS (name) VALUES (?)", (name,))
        return cls.get_by_id(year_group_id)

    def rename(self, new_name: str):
        if not new_name:
            raise ValueError("Year group name cannot be blank!")
        if query_one("SELECT * FROM YEAR_GROUPS WHERE name = ? AND id != ?", (new_name, self.id)):
            raise ValueError("Year group name already exists!")

        execute("UPDATE YEAR_GROUPS SET name = ? WHERE id = ?", (new_name, self.id))
        self.name = new_name
        return self
    
    def add_student(self, student: Student):
        if student.role != UserRole.STUDENT:
            raise ValueError("Only students can be added to a year group!")
        execute("UPDATE USERS SET year_group_id = ? WHERE id = ?", (self.id, student.id))
        student.year_group_id = self.id
        return self

    def remove_student(self, student: Student):
        if student.role != UserRole.STUDENT:
            raise ValueError("Only students can be removed from a year group!")
        if student.year_group_id != self.id:
            raise ValueError("Student is not in this year group!")

        execute("UPDATE USERS SET year_group_id = NULL WHERE id = ?", (student.id,))
        student.year_group_id = None
        return self

    def get_students(self):
        rows = query("SELECT * FROM USERS WHERE year_group_id = ?", (self.id,))
        students = []
        for row in rows:
            students.append(Student._from_row(row))
        return students
    
    def delete(self):
        if query_one("SELECT * FROM USERS WHERE year_group_id = ?", (self.id,)):
            raise ValueError("Cannot delete a year group that has students assigned to it!")
        execute("DELETE FROM YEAR_GROUPS WHERE id = ?", (self.id,))
        return True

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM YEAR_GROUPS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls(row['id'], row['name'])