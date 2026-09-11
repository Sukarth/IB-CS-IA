from .assignment import Assignment
from .enums import AssignmentType
from datetime import datetime

class GeneralAssignment(Assignment):
    def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, type: AssignmentType | None = None):
        super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published, type=AssignmentType.GENERAL)

    