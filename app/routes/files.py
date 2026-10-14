from flask import Blueprint, flash, g, redirect, url_for, abort, send_from_directory, current_app as app
from app.models.file_attachment import FileAttachment
from app.models.attachment import Attachment
from app.models.enums import UserRole
from app.models.classroom import Classroom
from app.models.assignment import Assignment
from app.models.material import Material
from app.models.submission import Submission
from app.database.uploads import remove_attachment
from app.security.decorators import check_login

bp = Blueprint('files', __name__, url_prefix='/files')
bp.before_request(check_login)

@bp.route('/download/<int:attachment_id>', methods=('GET',))
def download(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)
    classroom, submission = _check_attachment(attachment)

    if _can_view_attachment(classroom, submission) and isinstance(attachment, FileAttachment):
            return send_from_directory(app.config['UPLOAD_PATH'], attachment.stored_filename, as_attachment=True, download_name=attachment.original_filename)
    else:
        abort(404)


@bp.route('/delete/<int:attachment_id>', methods=('POST',))
def delete(attachment_id):
    attachment = Attachment.get_by_id(attachment_id)

    classroom, submission = _check_attachment(attachment)

    if not _can_delete_attachment(classroom, submission):
        abort(404)
    
    if submission:
        back_url = url_for('student.assignment', classroom_id=classroom.id, assignment_id=submission.assignment_id)
    else:
        back_url = url_for('teacher.material', material_id=attachment.material_id)
    
    if submission and submission.is_submitted:
        flash("Unsubmit the assignment first before removing its attachments.")
        return redirect(back_url)

    remove_attachment(attachment)
    flash("Attachment deleted successfully.")
    return redirect(back_url)


def _check_attachment(attachment):
    if not attachment:
        abort(404)

    classroom = None
    submission = None

    if attachment.material_id:
        material = Material.get_by_id(attachment.material_id)
        if material:
            classroom = Classroom.get_by_id(material.classroom_id)
    elif attachment.submission_id:
        submission = Submission.get_by_id(attachment.submission_id)
        if submission:
            assignment = Assignment.get_by_id(submission.assignment_id)
            if assignment:
                classroom = Classroom.get_by_id(assignment.classroom_id)

    return classroom, submission

def _can_view_attachment(classroom, submission):
    if g.user.role == UserRole.ADMIN:
        return True
    elif g.user.role == UserRole.TEACHER:
        return g.user.id == classroom.teacher_id if classroom else False
    elif g.user.role == UserRole.STUDENT:
        if submission:
            return g.user.id == submission.student_id
        return g.user.id in [student.id for student in classroom.get_students()] if classroom and classroom.is_published else False

def _can_delete_attachment(classroom, submission):
    if g.user.role == UserRole.ADMIN:
        return True
    elif g.user.role == UserRole.TEACHER:
        return g.user.id == classroom.teacher_id if classroom and not submission else False
    elif g.user.role == UserRole.STUDENT:
        if submission:
            return g.user.id == submission.student_id
        return False