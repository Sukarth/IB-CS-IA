from .assignment import Assignment
from .enums import AssignmentType
from .work_chunk import WorkChunk
from datetime import datetime
from app.database import execute, query, query_one

class Project(Assignment):
    TYPE = AssignmentType.PROJECT
    
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, min_group_size: int, max_group_size: int):
        super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published)
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, min_group_size: int, max_group_size: int):
        if min_group_size < 0:
            raise ValueError("Minimum group size cannot be smaller than zero!")
        if max_group_size < 1:
            raise ValueError("Maximum group size cannot be smaller than one!")
        if max_group_size < min_group_size:
            raise ValueError("Maximum group size must be bigger than the minimum group size!")
            
        return cls._insert(classroom_id, title, description, deadline, effort_hours, difficulty, is_published, min_group_size=min_group_size, max_group_size=max_group_size)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['classroom_id'], row['title'], row['description'], datetime.fromisoformat(row['deadline']), row['effort_hours'], row['difficulty'], bool(row['is_published']), row['min_group_size'], row['max_group_size'])

    def get_type_specific_details(self):
        return {'split_effort_hours': self.get_split_effort_hours(), 'min_group_size': self.min_group_size, 'max_group_size': self.max_group_size}

    def get_split_effort_hours(self):
        return [WorkChunk('Planning', self.effort_hours * 0.2), WorkChunk('Work', self.effort_hours * 0.5), WorkChunk('Review', self.effort_hours * 0.1) , WorkChunk('Presentation', self.effort_hours * 0.2)]
