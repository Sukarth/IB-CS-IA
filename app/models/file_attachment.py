from .attachment import Attachment
from .enums import AttachmentType
from app.database import query_one

class FileAttachment(Attachment):
    TYPE = AttachmentType.FILE
    
    def __init__(self, id: int, uploaded_by_id: int, stored_filename: str, original_filename: str, mime_type: str, file_size_kb: int):
        super().__init__(id, uploaded_by_id)
        self.stored_filename = stored_filename
        self.original_filename = original_filename
        self.mime_type = mime_type
        self.file_size_kb = file_size_kb

    @classmethod
    def create(cls, uploaded_in_id: int, uploaded_by_id: int, stored_filename: str, original_filename: str, mime_type: str, file_size_kb: int):
        if not stored_filename:
            raise ValueError("Stored filename cannot be blank!")
        if not original_filename:
            raise ValueError("Original filename cannot be blank!")
        if not mime_type:
            raise ValueError("MIME type cannot be blank!")
        if file_size_kb <= 0:
            raise ValueError("File size must be greater than zero!")

        if query_one("SELECT * FROM MATERIALS WHERE id = ?", (uploaded_in_id,)):
            return cls.get_by_id(cls._insert(uploaded_by_id, stored_filename=stored_filename, original_filename=original_filename, mime_type=mime_type, file_size_kb=file_size_kb, material_id=uploaded_in_id))
        elif query_one("SELECT * FROM SUBMISSIONS WHERE id = ?", (uploaded_in_id,)):
            return cls.get_by_id(cls._insert(uploaded_by_id, stored_filename=stored_filename, original_filename=original_filename, mime_type=mime_type, file_size_kb=file_size_kb, submission_id=uploaded_in_id))
        else:
            raise ValueError("Attachments can only be created in Materials or Submissions!")

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['uploaded_by'], row['stored_filename'], row['original_filename'], row['mime_type'], row['file_size_kb'])

    def get_type_specific_details(self):
        return {"stored_filename": self.stored_filename, "original_filename": self.original_filename, "mime_type": self.mime_type, "file_size_kb": self.file_size_kb}