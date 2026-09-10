from app.database import execute, query, query_one
from .enums import AssignmentType
from .completion_stats import CompletionStats
from datetime import datetime

class Assignment:
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, type: AssignmentType | None = None):
        self.id = id
        self.classroom_id = classroom_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.effort_hours = effort_hours
        self.difficulty = difficulty
        self.is_published = is_published
        self.type = type

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, type: AssignmentType | None = None):
        if not classroom_id:
            raise ValueError("Classroom ID cannot be blank!")
        if not query_one("SELECT * FROM CLASSROOMS WHERE id = ?", (classroom_id,)):
            raise ValueError("Classroom does not exist!")
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not deadline or deadline < datetime.now().isoformat():
            raise ValueError("Assignment deadline must be a future date!")
        if effort_hours <= 0:
            raise ValueError("Effort hours must be greater than zero!")
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5!")

        # THINK ABOUT HOW TO HANDLE CREATED_AT!!! and type of assignment
        
        assignment_id = execute("INSERT INTO ASSIGNMENTS (classroom_id, title, description, deadline, effort_hours, difficulty, is_published, created_at, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (classroom_id, title, description, deadline.isoformat(), effort_hours, difficulty, is_published, datetime.now().isoformat(), type.value if type else None))
        return cls.get_by_id(assignment_id)

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM ASSIGNMENTS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls(row['id'], row['classroom_id'], row['title'], row['description'], datetime.fromisoformat(row['deadline']), row['effort_hours'], row['difficulty'], bool(row['is_published']), AssignmentType(row['type']) if row['type'] else None) # return created at as well?
     
    def update(self, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, type: AssignmentType | None = None):
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not deadline or deadline < datetime.now().isoformat():
            raise ValueError("Assignment deadline must be a future date!")
        if effort_hours <= 0:
            raise ValueError("Effort hours must be greater than zero!")
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5!")
        
        self.title = title
        self.description = description
        self.deadline = deadline
        self.effort_hours = effort_hours
        self.difficulty = difficulty
        self.is_published = is_published
        self.type = type

        execute("UPDATE ASSIGNMENTS SET title = ?, description = ?, deadline = ?, effort_hours = ?, difficulty = ?, is_published = ?, type = ? WHERE id = ?", (self.title, self.description, self.deadline.isoformat(), self.effort_hours, self.difficulty, self.is_published, self.type.value if self.type else None, self.id))

    def publish(self):
        if self.is_published:
            raise ValueError("Assignment is already published!")
        
        self.is_published = True
        execute("UPDATE ASSIGNMENTS SET is_published = 1 WHERE id = ?", (self.id,))
    
    def unpublish(self):
        if not self.is_published:
            raise ValueError("Assignment is already unpublished!")
        
        self.is_published = False
        execute("UPDATE ASSIGNMENTS SET is_published = 0 WHERE id = ?", (self.id,))

    def delete(self):
        # NOT SAFE TO DELETE!! CHECK IF DATA PRESENT!
        execute("DELETE FROM ASSIGNMENTS WHERE id = ?", (self.id,))

    def days_remaining(self):
        delta = self.deadline - datetime.now().isoformat()
        return delta.days # negative if overdue

    def get_completion(self):
        return CompletionStats.get_by_assignment(self)

    def get_type_specific_details(self):
            return None

    def get_split_effort_hours(self):
        return None
    