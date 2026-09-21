from datetime import date
from .scheduled_block import ScheduledBlock
from ..models.enums import WarningType

class StudyPlan:
    def __init__(self, days: dict[date, list[ScheduledBlock]], warnings: list[tuple[str, WarningType, str]], generated_at: date):
        self.days = days
        self.warnings = warnings
        self.generated_at = generated_at