from .attachment import Attachment
from .enums import AttachmentType
from .enums import UploadArea
from urllib.parse import urlparse

class LinkAttachment(Attachment):
    TYPE = AttachmentType.LINK
    
    def __init__(self, id: int, uploaded_by_id: int,  url: str, link_text: str, material_id=None, submission_id=None):
        super().__init__(id, uploaded_by_id, material_id, submission_id)
        self.url = url
        self.link_text = link_text

    @classmethod
    def create(cls, uploaded_area_id: int, upload_area: UploadArea, uploaded_by_id: int, url: str, link_text: str):
        from .material import Material
        from .submission import Submission
        if not url:
            raise ValueError("URL cannot be blank!")
        parts = urlparse(url)
        if parts.scheme not in ('http', 'https') or not parts.hostname:
            raise ValueError("Invalid URL: " + url)
        if not link_text:
            raise ValueError("Link text cannot be blank!")
        if not uploaded_by_id:
            raise ValueError("Uploaded by ID cannot be blank!")

        if upload_area == UploadArea.MATERIALS:
            if not Material.get_by_id(uploaded_area_id):
                raise ValueError("Material does not exist!")
            return cls._insert(uploaded_by_id, url=url, link_text=link_text, material_id=uploaded_area_id)
        elif upload_area == UploadArea.SUBMISSIONS:
            if not Submission.get_by_id(uploaded_area_id):
                raise ValueError("Submission does not exist!")
            return cls._insert(uploaded_by_id, url=url, link_text=link_text, submission_id=uploaded_area_id)
        else:
            raise ValueError("Attachments can only be created in Materials or Submissions!")

    @classmethod
    def _from_row(cls, row):
        return cls(row['id'], row['uploaded_by_id'], row['url'], row['link_text'], row['material_id'], row['submission_id'])

    def get_type_specific_details(self):
        return {"url": self.url, "link_text": self.link_text}