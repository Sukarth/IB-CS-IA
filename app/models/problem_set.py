from .assignment import Assignment
from .enums import AssignmentType
from .work_chunk import WorkChunk
from datetime import datetime
from app.database import execute, query, query_one

class ProblemSet(Assignment):
    TYPE = AssignmentType.PROBLEMSET
    
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, number_of_problems: int):
        super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published)
        self.number_of_problems = number_of_problems

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, number_of_problems: int):
        if not number_of_problems:
            raise ValueError("Number of problems cannot be blank!")
        if number_of_problems < 0:
            raise ValueError("Number of problems must not be negative!")
        
        return cls._insert(classroom_id, title, description, deadline, effort_hours, difficulty, is_published, number_of_problems=number_of_problems)
        
    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['classroom_id'], row['title'], row['description'], datetime.fromisoformat(row['deadline']), row['effort_hours'], row['difficulty'], bool(row['is_published']), row['number_of_problems'])

    def get_type_specific_details(self):
        return {'split_effort_hours': self.get_split_effort_hours(), 'number_of_problems': self.number_of_problems}

    def get_split_effort_hours(self):
        return [WorkChunk('Problem Solving', self.effort_hours * 0.7), WorkChunk('Review', self.effort_hours * 0.3)]
