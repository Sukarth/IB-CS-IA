from enum import Enum

class UserRole(str, Enum):
    STUDENT = 'STUDENT'
    TEACHER = 'TEACHER'
    ADMIN = 'ADMIN'

class AssignmentType(str, Enum):
    GENERAL = 'GENERAL'
    ESSAY = 'ESSAY'
    PROBLEMSET = 'PROBLEMSET'
    PROJECT = 'PROJECT'

class AttachmentType(str, Enum):
    FILE = 'FILE'
    LINK = 'LINK'

class ProgressStatus(str, Enum):
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    NEEDS_HELP = 'NEEDS_HELP'

class UploadArea(str, Enum):
    MATERIALS = 'MATERIALS'
    SUBMISSIONS = 'SUBMISSIONS'

class WarningType(str, Enum):
    OVERDUE = 'OVERDUE'
    CANNOT_FINISH = 'CANNOT_FINISH'