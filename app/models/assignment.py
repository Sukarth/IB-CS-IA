from app.database import execute, query, query_one
from .enums import AssignmentType
from .completion_stats import CompletionStats
from datetime import datetime
from .work_chunk import WorkChunk

class Assignment:
    TYPE = None
    
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool):
        self.id = id
        self.classroom_id = classroom_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.effort_hours = effort_hours
        self.difficulty = difficulty
        self.is_published = is_published

    @classmethod
    def _insert(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, **extra):
        if cls.TYPE is None:
            raise TypeError("Assignment is abstract. Use a subclass")
        if not classroom_id:
            raise ValueError("Classroom ID cannot be blank!")
        if not query_one("SELECT * FROM CLASSROOMS WHERE id = ?", (classroom_id,)):
            raise ValueError("Classroom does not exist!")
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not deadline or deadline < datetime.now():
            raise ValueError("Assignment deadline must be a future date!")
        if effort_hours <= 0:
            raise ValueError("Effort hours must be greater than zero!")
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5!")

        columns = ['classroom_id', 'title', 'description', 'deadline', 'effort_hours', 'difficulty', 'is_published', 'type', 'created_at'] + list(extra)
        values = [classroom_id, title, description, deadline.isoformat(), effort_hours, difficulty, is_published, cls.TYPE.value, datetime.now().isoformat()] + list(extra.values())
        placeholders = ', '.join('?' for _ in columns)

        assignment_id = execute("INSERT INTO ASSIGNMENTS (" + ', '.join(columns) + ") VALUES (" + placeholders + ")", values)
        return cls.get_by_id(assignment_id)

    @classmethod
    def get_by_id(cls, id: int):
        row = query_one("SELECT * FROM ASSIGNMENTS WHERE id = ?", (id,))
        if not row:
            return None
        
        return cls._from_row(row)
     
    def update(self, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool):
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not deadline or deadline < datetime.now():
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

        execute("UPDATE ASSIGNMENTS SET title = ?, description = ?, deadline = ?, effort_hours = ?, difficulty = ?, is_published = ? WHERE id = ?", (self.title, self.description, self.deadline.isoformat(), self.effort_hours, self.difficulty, self.is_published, self.id))

    @classmethod
    def _from_row(cls, row):
        from .general_assignment import GeneralAssignment
        from .essay import Essay
        from .problem_set import ProblemSet
        from .project import Project
        assignment_typer = {AssignmentType.GENERAL: GeneralAssignment, AssignmentType.ESSAY: Essay, AssignmentType.PROBLEMSET: ProblemSet, AssignmentType.PROJECT: Project}
        return assignment_typer[AssignmentType(row['type'])]._from_row(row)

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
        if self.get_completion().completion_count > 0:
            raise ValueError("Cannot delete an assignment that has submissions!")
        # WHERE ARE THE HELP REQUESTS???????????????
        execute("DELETE FROM ASSIGNMENTS WHERE id = ?", (self.id,))

    def days_remaining(self):
        delta = self.deadline - datetime.now()
        return delta.days # negative if overdue

    def get_completion(self):
        return CompletionStats.get_by_assignment(self)

    def get_type(self):
        return self.TYPE

    def get_type_specific_details(self):
            return None

    def get_split_effort_hours(self):
        return [WorkChunk('Total', self.effort_hours)]
    