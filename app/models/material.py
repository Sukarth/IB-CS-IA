from .assignment import Assignment
from .enums import AssignmentType
from .enums import UploadArea
from .work_chunk import WorkChunk
from datetime import datetime
from app.database import execute, query, query_one

class Material:
    def __init__(self, id: int, title: str, description: str, classroom_id: int, uploaded_by_id: int):
        self.id = id
        self.title = title
        self.description = description
        self.classroom_id = classroom_id
        self.uploaded_by_id = uploaded_by_id

    @classmethod
    def create(cls, title: str, description: str, classroom_id: int, uploaded_by_id: int):
        if not title:
            raise ValueError("Material title cannot be blank!")
        if not classroom_id:
            raise ValueError("Classroom ID cannot be blank!")
        if not uploaded_by_id:
            raise ValueError("Uploaded by ID cannot be blank!")
        if not query_one("SELECT * FROM CLASSROOMS WHERE id = ?", (classroom_id,)):
            raise ValueError("Classroom does not exist!")

        return cls.get_by_id(execute("INSERT INTO MATERIALS (title, description, classroom_id, uploaded_by_id, uploaded_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, classroom_id, uploaded_by_id, datetime.now().isoformat())))
    
    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['title'], row['description'], row['classroom_id'], uploaded_by_id=row['uploaded_by_id'])

    @classmethod
    def get_by_id(cls, material_id: int):
        row = query_one("SELECT * FROM MATERIALS WHERE id = ?", (material_id,))
        if not row:
            return None
        return cls._from_row(row)
    
    def update(self, title: str, description: str):
        if not title:
            raise ValueError("Material title cannot be blank!")
        
        execute("UPDATE MATERIALS SET title = ?, description = ? WHERE id = ?", (title, description, self.id))
        self.title = title
        self.description = description
        return self

    def delete(self):
        if query_one("SELECT * FROM ATTACHMENTS WHERE material_id = ?", (self.id,)):
            raise ValueError("Cannot delete a material with attachments. Please remove attachments first.")
        execute("DELETE FROM MATERIALS WHERE id = ?", (self.id,))
        return True

    def get_attachments(self):
        from .attachment import Attachment
        return [Attachment._from_row(row) for row in query("SELECT * FROM ATTACHMENTS WHERE material_id = ?", (self.id,))]
    
    def attach_file(self, uploaded_by_id: int, stored_filename: str, original_filename: str, mime_type: str, file_size_kb: int):
        from .file_attachment import FileAttachment
        
        return FileAttachment.create(self.id, UploadArea.MATERIALS, uploaded_by_id, stored_filename, original_filename, mime_type, file_size_kb)
    
    def attach_link(self, uploaded_by_id: int, url: str, link_text: str):
        from .link_attachment import LinkAttachment
        
        return LinkAttachment.create(self.id, UploadArea.MATERIALS, uploaded_by_id, url, link_text)