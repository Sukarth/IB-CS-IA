from flask import Blueprint, g, redirect, render_template, url_for, flash, request, abort, current_app as app, send_from_directory
from app.security.decorators import check_role
from app.models.enums import UserRole
from app.models.assignment import Assignment
from app.models.user import User
from app.algorithms.study_scheduler import build_study_schedule
from app.models.student_settings import StudentSettings
from app.models.classroom import Classroom
from app.models.submission import Submission
from app.models.progress_record import ProgressRecord
from app.models.help_request import HelpRequest
from app.models.enums import ProgressStatus
from app.models.file_attachment import FileAttachment
from app.models.link_attachment import LinkAttachment
from app.models.material import Material
from app.models.attachment import Attachment
from app.models.enums import UploadArea
from app.database.uploads import upload_files, check_files, _delete_file, remove_attachment
from urllib.parse import urlparse

import calendar
from datetime import date

bp = Blueprint('student', __name__, url_prefix='/student')
bp.before_request(check_role(UserRole.STUDENT.value))

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('student.dashboard'))

@bp.route('/dashboard')
def dashboard():
    classrooms = [(c, User.get_by_id(c.teacher_id)) for c in g.user.get_classrooms()]
    assignments = Assignment.get_for_student(g.user.id)
    return render_template('student/dashboard.html', classrooms=classrooms, assignments=assignments)


@bp.route('/schedule')
def schedule():
    try:
        today = date.today()
        year  = request.args.get('year',  today.year,  type=int)
        month = request.args.get('month', today.month, type=int)

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        shown_date = date(year, month, 1)
        study_schedule = build_study_schedule(g.user)
        weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
        assignments = {a.id: a for a in Assignment.get_for_student(g.user.id)}
    except ValueError as ve:
        flash(str(ve))
        return render_template('student/schedule.html', study_schedule={}, weeks=[], assignments={}, today=today, month=month, day_abbr=list(calendar.day_abbr), prev_month=prev_month, prev_year=prev_year, next_month=next_month, next_year=next_year, year=year, shown_date=today)

    return render_template('student/schedule.html', study_schedule=study_schedule, weeks=weeks, assignments=assignments, today=today, month=month, day_abbr=list(calendar.day_abbr), prev_month=prev_month, prev_year=prev_year, next_month=next_month, next_year=next_year, year=year, shown_date=shown_date)

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    days = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    student_settings = StudentSettings.get_by_student_id(g.user.id)

    form = {'procrastination_factor': student_settings.procrastination_factor, 'exclude_overdue': student_settings.exclude_overdue}
    for day in days:
        form['hours_free_' + day] = getattr(student_settings, 'hours_free_' + day)

    if request.method == 'POST':
        form = {key: request.form.get(key, False) for key in form}
        form['exclude_overdue'] = 'exclude_overdue' in request.form

        try:
            student_settings.update_settings(float(form['procrastination_factor']), bool(form['exclude_overdue']), *[float(form['hours_free_' + day]) for day in days])
            flash('Settings updated successfully.')
            return redirect(url_for('student.settings'))
        except ValueError as ve:
            flash(str(ve))

    return render_template('student/settings.html', form=form)

@bp.route('/classroom/<int:classroom_id>/', methods=('GET',))
def classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    all_assignments = classroom.get_assignments(published_only=True)
    materials = classroom.get_materials()
    to_do_ids = {a.id for a in Assignment.get_for_student(g.user.id)}
    to_do = [a for a in all_assignments if a.id in to_do_ids]
    submitted = [a for a in all_assignments if a.id not in to_do_ids]
    teacher = User.get_by_id(classroom.teacher_id)
    return render_template('student/classroom.html', classroom=classroom, to_do=to_do, submitted=submitted, teacher=teacher, materials=materials)

@bp.route('/classroom/<int:classroom_id>/material/<int:material_id>/', methods=('GET',))
def material(classroom_id, material_id):
    classroom = _check_classroom(classroom_id)
    material = Material.get_by_id(material_id)
    if not material or material.classroom_id != classroom_id:
        abort(404)
    attachments = material.get_attachments()
    return render_template('student/material.html', classroom=classroom, material=material, attachments=attachments)

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/', methods=('GET',))
def assignment(classroom_id, assignment_id):
    assignment, classroom = _check_assignment(assignment_id, classroom_id)
    submission = Submission.get_by_student_and_assignment(g.user, assignment)
    progress = ProgressRecord.get_or_create(g.user, assignment)
    attachments = submission.get_attachments() if submission else []
    return render_template('student/assignment.html', assignment=assignment, classroom=classroom, submission=submission, attachments=attachments, progress=progress, statuses=(ProgressStatus.NOT_STARTED, ProgressStatus.IN_PROGRESS))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/submit', methods=('POST',))
def submit_assignment(classroom_id, assignment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    files = [f for f in request.files.getlist('files') if f.filename]
    urls = [u.rstrip(',') for u in request.form.get('links', '').split() if u.rstrip(',')]

    try:
        for url in urls:
            parts = urlparse(url)
            if parts.scheme not in ('http', 'https') or not parts.hostname: 
                raise ValueError("Invalid URL: " + url)
        if len(urls) > app.config['MAX_LINKS']:
            raise ValueError(f"Link attachment limit exceeded. You can attach a maximum of {app.config['MAX_LINKS']} links.")
        
        if files:
           check_files(files)

        existing_submission = Submission.get_by_student_and_assignment(g.user, assignment)
        existing_attachments = 0
        if existing_submission:
            existing_attachments = len(existing_submission.get_attachments())
        if not files and not urls and existing_attachments == 0:
            raise ValueError("You must attach at least one file or link to submit the assignment.")

        submission = Submission.submit(assignment, g.user)
        if files:
            uploaded_files = upload_files(files)
            for filename, stored_filename, mime_type, file_size_kb in uploaded_files:
                try:
                    FileAttachment.create(submission.id, UploadArea.SUBMISSIONS, g.user.id, stored_filename, filename, mime_type, file_size_kb)
                except Exception as e:
                    _delete_file(stored_filename)
                    submission.unsubmit()
                    raise ValueError(f"Error occurred while creating file attachments: {e}")
        for url in urls:
            LinkAttachment.create(submission.id, UploadArea.SUBMISSIONS, g.user.id, url, urlparse(url).hostname or url)
        flash('Assignment submitted successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/unsubmit', methods=('POST',))
def unsubmit_assignment(classroom_id, assignment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    try:
        submission = Submission.get_by_student_and_assignment(g.user, assignment)
        if not submission:
            raise ValueError("No submission found to unsubmit.")
        submission.unsubmit()
        flash('Assignment unsubmitted successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/progress', methods=('POST',))
def update_progress(classroom_id, assignment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    try:
        progress = ProgressRecord.get_or_create(g.user, assignment)
        new_status = request.form.get('status', type=ProgressStatus)
        notes = request.form.get('notes', '')
        hours_to_add = request.form.get('hours_to_add', type=float)

        if new_status not in (ProgressStatus.NOT_STARTED, ProgressStatus.IN_PROGRESS):
            raise ValueError("Invalid status.")
        if progress.status == ProgressStatus.COMPLETED:
            raise ValueError("Unsubmit the assignment before changing its progress.")

        if hours_to_add is None:
            raise ValueError("Hours to add is required.")
        
        progress.log_hours(hours_to_add)
        
        progress.set_status(new_status, notes)
        flash('Progress updated successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/help', methods=('POST',))
def request_help(classroom_id, assignment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    try:
        message = request.form.get('help_request', '')
        is_urgent = 'is_urgent' in request.form
        HelpRequest.create(g.user, assignment, message, is_urgent)
        flash('Help request sent successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/download_attachment/<int:attachment_id>', methods=('GET',))
def download_attachment(classroom_id, assignment_id, attachment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    try:
        attachment = Attachment.get_by_id(attachment_id)
        submission = Submission.get_by_student_and_assignment(g.user, assignment)
        if not attachment or not submission or attachment.submission_id != submission.id:
            raise ValueError("Attachment not found for this assignment.")
        if isinstance(attachment, FileAttachment):
            return send_from_directory(app.config['UPLOAD_PATH'], attachment.stored_filename, as_attachment=True, download_name=attachment.original_filename)
        else:
            raise ValueError("Only file attachments can be downloaded.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

@bp.route('/classroom/<int:classroom_id>/assignment/<int:assignment_id>/delete_attachment/<int:attachment_id>', methods=('POST',))
def delete_attachment(classroom_id, assignment_id, attachment_id):
    assignment, _ = _check_assignment(assignment_id, classroom_id)
    try:
        attachment = Attachment.get_by_id(attachment_id)
        submission = Submission.get_by_student_and_assignment(g.user, assignment)
        if not attachment or not submission or attachment.submission_id != submission.id:
            raise ValueError("Attachment not found for this assignment.")
        if submission.is_submitted:
            raise ValueError("Cannot delete attachments from a submitted assignment. Please unsubmit first.")
        remove_attachment(attachment)
        flash('Attachment deleted successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('student.assignment', classroom_id=classroom_id, assignment_id=assignment_id))

def _check_assignment(assignment_id, classroom_id):
    assignment = Assignment.get_by_id(assignment_id)
    classroom = _check_classroom(classroom_id)
    if not assignment or not assignment.is_published or assignment.classroom_id != classroom_id or not classroom:
        abort(404)
    return assignment, classroom

def _check_classroom(classroom_id):
    classroom = Classroom.get_by_id(classroom_id)
    if not classroom or classroom_id not in [c.id for c in g.user.get_classrooms()]:
        abort(404)
    return classroom