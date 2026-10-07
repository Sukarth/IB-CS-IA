import os
import uuid
import filetype
import mimetypes
from werkzeug.utils import secure_filename
from flask import current_app as app
from app.database import execute, query_one
from math import ceil
from app.models.enums import AttachmentType
from pathlib import Path

def check_files(files):
    """
    Validates the uploaded files.
    """
    if not files:
        raise ValueError("No file(s) provided for upload.")
    if len(files) > app.config['MAX_FILES']:
        raise ValueError(f"File upload limit exceeded. You can upload a maximum of {app.config['MAX_FILES']} files. Compress your files into a single zip file if you need to upload many files.")
    total_size = 0
    for file in files:
        if not file:
            raise ValueError("Empty files can not be uploaded")
        file.stream.seek(0, 2)
        file_size = file.stream.tell()
        if file_size == 0:
            raise ValueError("Empty files can not be uploaded")
        total_size += file_size
        file.stream.seek(0)

    if total_size > app.config['MAX_CONTENT_LENGTH']:
        raise ValueError(f"Total file(s) size exceeds the maximum limit of {app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)} MB.")
    
    for file in files:
        if file.filename == '':
            raise ValueError("File(s) must have a valid filename.")
        
        if _get_type(file)[1] not in app.config['UPLOAD_EXTENSIONS']:
            raise ValueError(f"File type not allowed: {file.filename}")
    return True

def upload_files(files):
    """
    Uploads a file to the server and returns the file path.
    """
    uploaded_files = []
    for file in files:
        filename = secure_filename(file.filename)
        mime_type, extension = _get_type(file)
        stored_filename = f"{uuid.uuid4().hex}{extension}"
        file.stream.seek(0, 2)
        size_kb = max(1, ceil(file.stream.tell() / 1024))
        file.stream.seek(0)
        file_path = os.path.join(app.config['UPLOAD_PATH'], stored_filename)
        uploaded_files.append((filename, stored_filename, mime_type, size_kb))

        file.save(file_path)

    return uploaded_files

def _delete_file(stored_filename):
    """
    Deletes a file from the server.
    """
    file_path = os.path.join(app.config['UPLOAD_PATH'], stored_filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            raise OSError(f"Error occurred while deleting file: {stored_filename}") from e
    return True
    
def remove_attachment(attachment):
    attachment.delete()
    if attachment.TYPE == AttachmentType.FILE:
        _delete_file(attachment.stored_filename)

def _get_type(file):
    ALLOWED_TEXT_EXTENSIONS = {'.py', '.txt', '.java', '.c', '.cpp', '.js', '.html', '.css'}

    kind = filetype.guess(file.stream.read(261))
    file.stream.seek(0)
    if kind:
        return kind.mime, '.' + kind.extension
    
    extension = Path(file.filename).suffix.lower()
    if extension in ALLOWED_TEXT_EXTENSIONS:
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type:
            return mime_type, mimetypes.guess_extension(mime_type) or extension
        else:
            return 'text/plain', extension
    raise ValueError(f"Could not determine the file type for: {file.filename}")
