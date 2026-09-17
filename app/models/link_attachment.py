from .attachment import Attachment
from .enums import AttachmentType
from app.database import query_one

class LinkAttachment(Attachment):
    TYPE = AttachmentType.LINK
    
    def __init__(self, id: int, uploaded_by_id: int, url: str, link_text: str):
        super().__init__(id, uploaded_by_id)
        self.url = url
        self.link_text = link_text

    @classmethod
    def create(cls, uploaded_in_id: int, uploaded_by_id: int, url: str, link_text: str):
        if not url:
            raise ValueError("URL cannot be blank!")
        if not link_text:
            raise ValueError("Link text cannot be blank!")

        if query_one("SELECT * FROM MATERIALS WHERE id = ?", (uploaded_in_id,)):
            return cls.get_by_id(cls._insert(uploaded_by_id, url=url, link_text=link_text, material_id=uploaded_in_id))
        elif query_one("SELECT * FROM SUBMISSIONS WHERE id = ?", (uploaded_in_id,)):
            return cls.get_by_id(cls._insert(uploaded_by_id, url=url, link_text=link_text, submission_id=uploaded_in_id))
        else:
            raise ValueError("Attachments can only be created in Materials or Submissions!")

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['uploaded_by'], row['url'], row['link_text'])

    def get_type_specific_details(self):
        return {"url": self.url, "link_text": self.link_text}