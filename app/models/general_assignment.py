from .assignment import Assignment
from .enums import AssignmentType
from datetime import datetime

class GeneralAssignment(Assignment):
    TYPE = AssignmentType.GENERAL

    @classmethod
    def _from_row(cls, row):
        return cls(id=row['id'], classroom_id=row['classroom_id'], title=row['title'], description=row['description'], deadline=datetime.fromisoformat(row['deadline']), effort_hours=row['effort_hours'], difficulty=row['difficulty'], is_published=bool(row['is_published']))
    