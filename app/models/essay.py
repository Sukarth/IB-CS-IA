from .assignment import Assignment
from .enums import AssignmentType
from .work_chunk import WorkChunk
from datetime import datetime
from app.database import execute, query, query_one

class Essay(Assignment):
    TYPE = AssignmentType.ESSAY
    
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, word_limit: int):
        super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published)
        self.word_limit = word_limit

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool, word_limit: int):
        if not word_limit:
            raise ValueError("Word limit cannot be blank!")
        if word_limit < 0:
            raise ValueError("Word limit must not be negative!")
        
        return cls._insert(classroom_id, title, description, deadline, effort_hours, difficulty, is_published, word_limit=word_limit)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['classroom_id'], row['title'], row['description'], datetime.fromisoformat(row['deadline']), row['effort_hours'], row['difficulty'], bool(row['is_published']), row['word_limit'])

    def get_type_specific_details(self):
        return {'split_effort_hours': self.get_split_effort_hours(), 'word_limit': self.word_limit}

    def get_split_effort_hours(self):
        return [WorkChunk('Research', self.effort_hours * 0.4), WorkChunk('Writing', self.effort_hours * 0.5), WorkChunk('Review and Refinement', self.effort_hours * 0.1)]
