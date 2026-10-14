from app.database import execute, query, query_one
from .enums import AssignmentType
from .completion_stats import CompletionStats
from datetime import datetime
from abc import ABC, abstractmethod
import math

class Assignment(ABC):
    TYPE = None
    
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool):
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
        from .classroom import Classroom
        title = title.strip()
        if cls.TYPE is None:
            raise TypeError("Assignment is abstract. Use a subclass!")
        if not classroom_id:
            raise ValueError("Classroom ID cannot be blank!")
        if not Classroom.get_by_id(classroom_id):
            raise ValueError("Classroom does not exist!")
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not deadline or deadline < datetime.now():
            raise ValueError("Assignment deadline must be a future date!")
        if not math.isfinite(effort_hours):
            raise ValueError("Effort hours must be a valid finite number!")
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
     
    def _update(self, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, **extra):
        title = title.strip()
        if not title:
            raise ValueError("Assignment title cannot be blank!")
        if not math.isfinite(effort_hours):
            raise ValueError("Effort hours must be a valid finite number!")
        if effort_hours <= 0:
            raise ValueError("Effort hours must be greater than zero!")
        if not deadline:
            raise ValueError("Assignment deadline cannot be blank!")
        if difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be between 1 and 5!")

        columns = ['title', 'description', 'deadline', 'effort_hours', 'difficulty'] + list(extra)
        values = [title, description, deadline.isoformat(), effort_hours, difficulty] + list(extra.values())
        inp = ', '.join(f'{col} = ?' for col in columns)

        execute("UPDATE ASSIGNMENTS SET " + inp + " WHERE id = ?", values + [self.id])

        self.title = title
        self.description = description
        self.deadline = deadline
        self.effort_hours = effort_hours
        self.difficulty = difficulty

        return self

    @classmethod
    def _from_row(cls, row):
        from .general_assignment import GeneralAssignment
        from .essay import Essay
        from .problem_set import ProblemSet
        from .project import Project
        
        assignment_typer = {AssignmentType.GENERAL: GeneralAssignment, AssignmentType.ESSAY: Essay, AssignmentType.PROBLEMSET: ProblemSet, AssignmentType.PROJECT: Project}
        
        return assignment_typer[AssignmentType(row['type'])]._from_row(row)

    @classmethod
    def get_for_student(cls, student_id: int):
        """Get all schedulable assignments for a specific student."""
        rows = query("SELECT ASSIGNMENTS.* FROM ASSIGNMENTS INNER JOIN ENROLLMENTS ON ASSIGNMENTS.classroom_id = ENROLLMENTS.classroom_id INNER JOIN CLASSROOMS ON ASSIGNMENTS.classroom_id = CLASSROOMS.id WHERE ENROLLMENTS.student_id = ? AND ASSIGNMENTS.is_published = ? AND CLASSROOMS.is_published = ? AND ASSIGNMENTS.id NOT IN (SELECT assignment_id FROM SUBMISSIONS WHERE student_id = ? AND is_submitted = ?)", (student_id, True, True, student_id, True))
        if not rows:
            return []
        return [cls._from_row(row) for row in rows]

    def publish(self):
        if self.is_published:
            raise ValueError("Assignment is already published!")
        
        self.is_published = True
        execute("UPDATE ASSIGNMENTS SET is_published = ? WHERE id = ?", (True, self.id))
        return self

    def unpublish(self):
        if not self.is_published:
            raise ValueError("Assignment is already unpublished!")
        
        self.is_published = False
        execute("UPDATE ASSIGNMENTS SET is_published = ? WHERE id = ?", (False, self.id))
        return self

    def delete(self):
        from .help_request import HelpRequest
        if query_one("SELECT * FROM SUBMISSIONS WHERE assignment_id = ?", (self.id,)):
            raise ValueError("Cannot delete an assignment that has submissions!")
        if HelpRequest.get_for_assignment(self.id):
            raise ValueError("Cannot delete an assignment that has help requests!")

        execute("DELETE FROM ASSIGNMENTS WHERE id = ?", (self.id,))
        return True

    def days_remaining(self):
        return (self.deadline - datetime.now()).total_seconds()/86400

    def get_completion(self):
        return CompletionStats.get_by_assignment(self)

    def get_type(self):
        return self.TYPE

    @abstractmethod
    def get_type_specific_details(self):
        ...

    @abstractmethod
    def get_split_effort_hours(self):
        ...
    