from datetime import datetime
from app.database import execute, query, query_one
from .enums import UploadArea, UserRole, ProgressStatus
from .assignment import Assignment
from .student import Student
from .classroom import Classroom

class Submission:
    def __init__(self, id: int, assignment_id: int, student_id: int, is_submitted: bool, submitted_at: datetime | None, version: int, feedback: str):
        self.id = id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.is_submitted = is_submitted
        self.submitted_at = submitted_at
        self.version = version
        self.feedback = feedback

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['assignment_id'], row['student_id'], bool(row['is_submitted']), datetime.fromisoformat(row['submitted_at']) if row['submitted_at'] else None, row['version'], row['feedback'])

    @classmethod
    def get_by_student_and_assignment(cls, student: Student, assignment: Assignment):
        row = query_one("SELECT * FROM SUBMISSIONS WHERE assignment_id = ? AND student_id = ?", (assignment.id, student.id))
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    def get_by_id(cls, submission_id: int):
        row = query_one("SELECT * FROM SUBMISSIONS WHERE id = ?", (submission_id,))
        if not row:
            return None
        return cls._from_row(row)
    
    @classmethod
    def submit(cls, assignment: Assignment, student: Student):
        from .progress_record import ProgressRecord
        
        if not student or student.role != UserRole.STUDENT:
            raise ValueError("Only students can submit assignments!")
        
        if not assignment:
            raise ValueError("Assignment does not exist.")

        classroom = Classroom.get_by_id(assignment.classroom_id)
        if not classroom:
            raise ValueError("Classroom does not exist.")

        if not classroom.is_published:
            raise ValueError("Cannot submit assignment for an unpublished classroom.")

        if not assignment.is_published:
            raise ValueError("Cannot submit assignment for an unpublished assignment.")

        existing_submission = cls.get_by_student_and_assignment(student, assignment)

        if existing_submission:
            if existing_submission.is_submitted:
                raise ValueError("Assignment is already submitted.")
            else:
                execute("UPDATE SUBMISSIONS SET is_submitted = ?, submitted_at = ?, version = ? WHERE id = ?", (True, datetime.now().isoformat(), existing_submission.version + 1, existing_submission.id))
                ProgressRecord.get_or_create(student, assignment).set_status(ProgressStatus.COMPLETED)
                return cls.get_by_id(existing_submission.id)
        else:
            execute("INSERT INTO SUBMISSIONS (assignment_id, student_id, is_submitted, submitted_at, version, feedback) VALUES (?, ?, ?, ?, ?, ?)", (assignment.id, student.id, True, datetime.now().isoformat(), 1, ""))
            ProgressRecord.get_or_create(student, assignment).set_status(ProgressStatus.COMPLETED)
            return cls.get_by_student_and_assignment(student, assignment)

    def unsubmit(self):
        from .user import User
        from .progress_record import ProgressRecord

        user = User.get_by_id(self.student_id)
        if not user or user.role != UserRole.STUDENT:
            raise ValueError("Only students can unsubmit assignments!")
        
        assignment = Assignment.get_by_id(self.assignment_id)
        if not assignment:
            raise ValueError("Assignment does not exist.")
        
        if not self.is_submitted:
            raise ValueError("Submission is not submitted.")
        execute("UPDATE SUBMISSIONS SET is_submitted = ? WHERE id = ?", (False, self.id))
        
        ProgressRecord.get_or_create(user, assignment).set_status(ProgressStatus.IN_PROGRESS)
        
        self.is_submitted = False
        return self

    def add_feedback(self, feedback: str):
        execute("UPDATE SUBMISSIONS SET feedback = ? WHERE id = ?", (feedback, self.id))
        self.feedback = feedback
        return self

    def attach_file(self, uploaded_by_id: int, stored_filename: str, original_filename: str, mime_type: str, file_size_kb: int):
        from .file_attachment import FileAttachment
        return FileAttachment.create(self.id, UploadArea.SUBMISSIONS, uploaded_by_id, stored_filename, original_filename, mime_type, file_size_kb)

    def attach_link(self, uploaded_by_id: int, url: str, link_text: str):
        from .link_attachment import LinkAttachment
        return LinkAttachment.create(self.id, UploadArea.SUBMISSIONS, uploaded_by_id, url, link_text)
    
    def get_attachments(self):
        from .attachment import Attachment
        rows = query("SELECT * FROM ATTACHMENTS WHERE submission_id = ?", (self.id,))
        return [Attachment._from_row(row) for row in rows]