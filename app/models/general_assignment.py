from .assignment import Assignment
from .enums import AssignmentType
from datetime import datetime
from .work_chunk import WorkChunk

class GeneralAssignment(Assignment):
    TYPE = AssignmentType.GENERAL

    @classmethod
    def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, is_published: bool):
        return cls._insert(classroom_id, title, description, deadline, effort_hours, difficulty, is_published)

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['classroom_id'], row['title'], row['description'],datetime.fromisoformat(row['deadline']), row['effort_hours'], row['difficulty'], bool(row['is_published']))
    
    def update(self, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int):
        self._update(title, description, deadline, effort_hours, difficulty)
        return self

    def get_split_effort_hours(self):
        return [WorkChunk('Total', self.effort_hours)]

    def get_type_specific_details(self):
        return {'split_effort_hours': self.get_split_effort_hours()}
    