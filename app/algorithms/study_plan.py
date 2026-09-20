from datetime import date
from ..models.work_chunk import WorkChunk
from ..models.assignment import Assignment
from .scheduled_block import ScheduledBlock

class StudyPlan:
    def __init__(self, days: dict[date, list[ScheduledBlock]], warnings: list[str], generated_at: date):
        self.days = days
        self.warnings = warnings
        self.generated_at = generated_at