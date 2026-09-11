from .assignment import Assignment
from .enums import AssignmentType
from datetime import datetime

class GeneralAssignment(Assignment):
    TYPE = AssignmentType.GENERAL

    