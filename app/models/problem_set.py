from .assignment import Assignment
from .enums import AssignmentType
from .work_chunk import WorkChunk
from datetime import datetime
from app.database import execute, query, query_one

class ProblemSet(Assignment):
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, number_of_problems: int, type: AssignmentType | None = None):
        super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published, type=AssignmentType.PROBLEMSET)
        self.number_of_problems = number_of_problems

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, number_of_problems: int, type: AssignmentType | None = None):
        if not number_of_problems:
            raise ValueError("Number of problems cannot be blank!")
        
        return super().create(classroom_id, title, description, deadline, effort_hours, difficulty, is_published, number_of_problems=number_of_problems)
        

    def get_type_specific_details(self):
        return {'work_chunk': self.WorkChunk, 'number_of_problems': self.number_of_problems}
