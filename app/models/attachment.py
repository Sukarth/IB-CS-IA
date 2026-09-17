from app.database import execute, query, query_one
from abc import ABC, abstractmethod
from datetime import datetime
from .enums import AttachmentType

class Attachment(ABC):
    TYPE = None
    
    def __init__(self, id: int, uploaded_by_id: int, material_id=None, submission_id=None):
        self.id = id
        self.uploaded_by_id = uploaded_by_id
        self.material_id = material_id
        self.submission_id = submission_id

    @classmethod
    def _insert(cls, uploaded_by_id: int, **extra):
        if cls.TYPE is None:
            raise TypeError("Attachment is abstract. Use a subclass!")
        if not uploaded_by_id:
            raise ValueError("Uploaded by ID cannot be blank!")

        columns = ['uploaded_by', 'kind', 'uploaded_at'] + list(extra)
        values = [uploaded_by_id, cls.TYPE.value, datetime.now().isoformat()] + list(extra.values())
        placeholders = ', '.join('?' for _ in columns)

        return cls.get_by_id(execute("INSERT INTO ATTACHMENTS (" + ', '.join(columns) + ") VALUES (" + placeholders + ")", values))

    @classmethod
    def get_by_id(cls, attachment_id: int):
        row = query_one("SELECT * FROM ATTACHMENTS WHERE id = ?", (attachment_id,))
        if not row:
            return None
        return cls._from_row(row)

    @classmethod
    def _from_row(cls, row):
        from .file_attachment import FileAttachment
        from .link_attachment import LinkAttachment
        
        attachment_typer = {AttachmentType.FILE.value: FileAttachment, AttachmentType.LINK.value: LinkAttachment}
        
        return attachment_typer[row['kind']]._from_row(row)

    def delete(self):
        execute("DELETE FROM ATTACHMENTS WHERE id = ?", (self.id,))
        return True

    @abstractmethod
    def get_type_specific_details(self):
        ...

    def get_type(self):
        return self.TYPE