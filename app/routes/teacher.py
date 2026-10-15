from datetime import datetime
from flask import Blueprint, g, redirect, render_template, url_for, abort, request, flash, current_app as app
from app.security.decorators import check_role
from app.models.enums import UserRole
from app.models.classroom import Classroom
from app.models.assignment import Assignment
from app.models.general_assignment import GeneralAssignment
from app.models.essay import Essay
from app.models.problem_set import ProblemSet
from app.models.project import Project
from app.models.help_request import HelpRequest
from app.models.submission import Submission
from app.models.progress_record import ProgressRecord
from app.models.completion_stats import CompletionStats
from app.models.enums import ProgressStatus
from app.models.user import User
from app.models.file_attachment import FileAttachment
from app.models.material import Material
from app.algorithms.help_queue import build_help_queue
from app.database.uploads import upload_files, check_files, _delete_file
from urllib.parse import urlparse

ASSIGNMENT_TYPES = {
    'GENERAL': (GeneralAssignment, []),
    'ESSAY': (Essay, ['word_limit']),
    'PROBLEMSET': (ProblemSet, ['number_of_problems']),
    'PROJECT': (Project, ['min_group_size', 'max_group_size'])
}

bp = Blueprint('teacher', __name__, url_prefix='/teacher')
bp.before_request(check_role(UserRole.TEACHER.value))

@bp.route('/dashboard')
def dashboard():
    classrooms =  [classroom for classroom in g.user.get_classrooms()]
    published_classrooms = [classroom for classroom in classrooms if classroom.is_published]
    unpublished_classrooms = [classroom for classroom in classrooms if not classroom.is_published]
    help_requests = []
    
    try:
        pq = build_help_queue(g.user)
        while not pq.is_empty():
            help_req = pq.dequeue()
            help_requests.append((help_req, User.get_by_id(help_req.student_id), Assignment.get_by_id(help_req.assignment_id)))
    except ValueError as ve:
        flash(str(ve))

    return render_template('teacher/dashboard.html', published_classrooms=published_classrooms, unpublished_classrooms=unpublished_classrooms, help_requests=help_requests)

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('teacher.dashboard'))

@bp.route('/classroom/<int:classroom_id>/', methods=('GET',))
def classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    unpublished_assignments = classroom.get_assignments(unpublished_only=True)
    published_assignments = classroom.get_assignments(published_only=True)
    materials = classroom.get_materials()
    students = classroom.get_students()
    help_reqs = classroom.get_help_requests()
    help_requests = [(help_req, User.get_by_id(help_req.student_id), Assignment.get_by_id(help_req.assignment_id)) for help_req in help_reqs]
    enrolled_student_ids = {student.id for student in students}
    available_students = [student for student in User.get_all(UserRole.STUDENT, activated=True) if student.id not in enrolled_student_ids]

    return render_template('teacher/classroom.html', classroom=classroom, unpublished_assignments=unpublished_assignments, published_assignments=published_assignments, materials=materials, students=students, help_requests=help_requests, available_students=available_students)

@bp.route('/classroom/create', methods=('POST',))
def create_classroom():
    name = request.form.get('classroom_name', '')
    description = request.form.get('classroom_description', '')
    is_published = request.form.get('is_published') == 'on'

    try:
        classroom = Classroom.create(name, description, g.user, is_published)
        flash("Classroom created successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.dashboard'))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/enroll', methods=('POST',))
def enroll_student(classroom_id):
    classroom = _check_classroom(classroom_id)
    student = User.get_by_id(request.form.get('enroll_student_id', type=int) or 0)
    try:
        if not student or student.role != UserRole.STUDENT:
            raise ValueError("No student with that ID was found.")
        classroom.enroll_student(student)
        flash(f"Student {student.name} enrolled successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))
    
    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/unenroll', methods=('POST',))
def unenroll_student(classroom_id):
    classroom = _check_classroom(classroom_id)
    student = User.get_by_id(request.form.get('unenroll_student_id', 0, type=int))
    try:
        if not student or student.role != UserRole.STUDENT:
            raise ValueError("No student with that ID was found.")
        classroom.unenroll_student(student)
        flash(f"Student {student.name} unenrolled successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/publish', methods=('POST',))
def publish_classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    try:
        classroom.publish()
        flash("Classroom published successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))
    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/unpublish', methods=('POST',))
def unpublish_classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    try:
        classroom.unpublish()
        flash("Classroom unpublished successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))
    
    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/edit', methods=('POST',))
def edit_classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    name = request.form.get('classroom_name', '')
    description = request.form.get('classroom_description', '')

    try:
        classroom.update(name, description)
        flash("Classroom updated successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/delete', methods=('POST',))
def delete_classroom(classroom_id):
    classroom = _check_classroom(classroom_id)
    try:
        classroom.delete()
        flash("Classroom deleted successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

    return redirect(url_for('teacher.dashboard'))

@bp.route('/classroom/<int:classroom_id>/analytics', methods=('GET',))
def classroom_analytics(classroom_id):
    classroom = _check_classroom(classroom_id)
    assignments = classroom.get_assignments(True)
    length = len(assignments)
    assignment_query = request.args.get('assignment_query', '').strip().lower()
    name_query = request.args.get('name_query', '').strip().lower()

    students = classroom.get_students()
    counts = {student.id: 0 for student in students}
    for assignment in assignments:
        for student in assignment.get_completion().completed_students:
            counts[student.id] += 1

    filtered_students = [(student, (counts[student.id] * 100) / length if length > 0 else 0) for student in classroom.get_students() if name_query in student.name.lower()]
    
    filtered_assignments = []
    for assignment in assignments:
        if assignment_query not in assignment.title.lower():
            continue

        completion_hours = []
        for student in students:
            progress = ProgressRecord.get_progress(student, assignment)
            if progress and progress.status == ProgressStatus.COMPLETED and progress.hours_completed > 0:
                completion_hours.append(progress.hours_completed)
        
        avg_actual_hours = sum(completion_hours) / len(completion_hours) if completion_hours else None
        hours_difference = avg_actual_hours - assignment.effort_hours if avg_actual_hours else None

        filtered_assignments.append((assignment, CompletionStats.get_by_assignment(assignment).completion_percentage, assignment.effort_hours, avg_actual_hours, hours_difference, len(completion_hours)))
    
    classroom_completion_stats = sorted(filtered_students, key=lambda row: (-row[1], row[0].name))
    assignment_completion_stats = sorted(filtered_assignments, key=lambda row: (row[1], row[0].title))

    # submissions that are submitted but still have no feedback
    empty_feedback_submissions = []
    for assignment in assignments:
        for student in students:
            submission = Submission.get_by_student_and_assignment(student, assignment)
            if submission and submission.is_submitted and not submission.feedback.strip():
                empty_feedback_submissions.append((submission, assignment, student))
    empty_feedback_submissions.sort(key=lambda row: row[0].submitted_at)
    
    return render_template('teacher/analytics.html', classroom=classroom, classroom_completion_stats=classroom_completion_stats, assignment_completion_stats=assignment_completion_stats, assignment_query=assignment_query, name_query=name_query, empty_feedback_submissions=empty_feedback_submissions)

@bp.route('/classroom/<int:classroom_id>/material/create', methods=('POST',))
def create_material(classroom_id):
    classroom = _check_classroom(classroom_id)
    title = request.form.get('material_title', '')
    description = request.form.get('material_description', '')
    files = [f for f in request.files.getlist('material_files') if f.filename]
    urls = [u.rstrip(',') for u in request.form.get('material_links', '').split() if u.rstrip(',')]
    
    try:
        for url in urls:
            parts = urlparse(url)
            if parts.scheme not in ('http', 'https') or not parts.hostname: 
                raise ValueError("Invalid URL: " + url)
        if len(urls) > app.config['MAX_LINKS']:
            raise ValueError(f"Link attachment limit exceeded. You can attach a maximum of {app.config['MAX_LINKS']} links.")
        
        if files:
            check_files(files)
        
        material = Material.create(title, description, classroom.id, g.user.id)

        if files:
            uploaded_files = upload_files(files)
            
            for filename, stored_filename, mime_type, file_size_kb in uploaded_files:
                try:
                    material.attach_file(g.user.id, stored_filename, filename, mime_type, file_size_kb)
                except Exception as e:
                    _delete_file(stored_filename)
                    material.delete()
                    raise ValueError(f"Error occurred while creating file attachments: {e}")
        for url in urls:
            material.attach_link(g.user.id, url, urlparse(url).hostname or url)
        
        flash('Material created successfully.')
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.classroom', classroom_id=classroom.id))
    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/classroom/<int:classroom_id>/assignment/create', methods=('POST',))
def create_assignment(classroom_id):
    classroom = _check_classroom(classroom_id)
    try:
        title = request.form.get('assignment_title', '')
        description = request.form.get('assignment_description', '')
        deadline = request.form.get('assignment_deadline', type=datetime.fromisoformat)
        if deadline is None:
            raise ValueError("Please enter a valid deadline.")
        effort_hours = float(request.form.get('assignment_effort_hours', 0, type=float))
        difficulty = int(request.form.get('assignment_difficulty', 0, type=int))
        is_published = request.form.get('assignment_is_published') == 'on'
        type = request.form.get('type', 'GENERAL')
        if type not in ASSIGNMENT_TYPES:
            raise ValueError("Invalid assignment type.")

        assignment_type, fields = ASSIGNMENT_TYPES[type]
        kwargs = {}
        for field in fields:
            value = request.form.get(field, type=int)
            if value is None:
                raise ValueError(f"Please enter a whole number for {field.replace('_', ' ')}.")
            kwargs[field] = value
        
        assignment_type.create(classroom.id, title, description, deadline, effort_hours, difficulty, is_published, **kwargs)
        flash('Assignment created successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/assignment/<int:assignment_id>/', methods=('GET',))
def assignment(assignment_id):
    assignment, classroom = _owns_assignment(assignment_id)
    completion_stats = CompletionStats.get_by_assignment(assignment)
    students = classroom.get_students()
    submissions = [Submission.get_by_student_and_assignment(student, assignment) for student in students]
    help_requests_students = [(help_request, User.get_by_id(help_request.student_id)) for help_request in HelpRequest.get_for_assignment(assignment.id)]
    resolved_help_requests_students = [i for i in help_requests_students if i[0].resolved_at]
    unresolved_help_requests_students = [i for i in help_requests_students if not i[0].resolved_at]
    submissions_students = zip(submissions, students)
    needs_help_count=len({student.id for _, student in unresolved_help_requests_students})

    status_counts = {status: 0 for status in ProgressStatus}
    for student in students:
        progress = ProgressRecord.get_progress(student, assignment)
        status_counts[progress.status if progress else ProgressStatus.NOT_STARTED] += 1
    
    return render_template('teacher/assignment.html', assignment=assignment, resolved_help_requests_students=resolved_help_requests_students, unresolved_help_requests_students=unresolved_help_requests_students, submissions_students=submissions_students, completion_stats=completion_stats, progress_rows=_progress_rows(assignment, classroom, g.user), not_started_count=status_counts[ProgressStatus.NOT_STARTED], in_progress_count=status_counts[ProgressStatus.IN_PROGRESS], completed_count=status_counts[ProgressStatus.COMPLETED], needs_help_count=needs_help_count)

@bp.route('/assignment/<int:assignment_id>/edit', methods=('POST',))
def edit_assignment(assignment_id):
    assignment, _ = _owns_assignment(assignment_id)

    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        deadline = request.form.get('deadline', type=datetime.fromisoformat)
        if deadline is None:
            raise ValueError("Please enter a valid deadline.")
        effort_hours = float(request.form.get('effort_hours', 0, type=float))
        difficulty = int(request.form.get('difficulty', 0, type=int))
        is_published = request.form.get('is_published') == 'on'

        kwargs = {}
        for field in ASSIGNMENT_TYPES[assignment.TYPE.value][1]:
            value = request.form.get(field, type=int)
            if value is None:
                raise ValueError(f"Please enter a whole number for {field.replace('_', ' ')}.")
            kwargs[field] = value
        
        assignment.update(title, description, deadline, effort_hours, difficulty, **kwargs)

        if is_published and not assignment.is_published:
            assignment.publish()
        elif not is_published and assignment.is_published:
            assignment.unpublish()
        
        flash('Assignment updated successfully.')
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.assignment', assignment_id=assignment.id))

    return redirect(url_for('teacher.assignment', assignment_id=assignment.id))

@bp.route('/assignment/<int:assignment_id>/delete', methods=('POST',))
def delete_assignment(assignment_id):
    assignment, classroom = _owns_assignment(assignment_id)
    try:
        assignment.delete()
        flash("Assignment deleted successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.assignment', assignment_id=assignment.id))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/help_request/<int:help_request_id>/', methods=('GET',))
def help_request(help_request_id):
    help_request, assignment, _ = _check_help_request(help_request_id)
    student = User.get_by_id(help_request.student_id)
    
    next_request = None
    pq = build_help_queue(g.user)
    while not pq.is_empty():
        help_req = pq.dequeue()
        if help_req.id != help_request.id:
            next_request = help_req
            break
    return render_template('teacher/help_request.html', help_request=help_request, assignment=assignment, student=student, next_request=next_request)

@bp.route('/help_request/<int:help_request_id>/resolve', methods=('POST',))
def resolve_help_request(help_request_id):
    help_request, _, _ = _check_help_request(help_request_id)

    resolution_notes = request.form.get('resolution_notes', '')
    try:
        help_request.resolve(g.user.id, resolution_notes)
        flash('Help request resolved successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('teacher.help_request', help_request_id=help_request.id))

@bp.route('/material/<int:material_id>', methods=('GET',))
def material(material_id):
    material, classroom = _check_material(material_id)
    attachments = material.get_attachments()
    return render_template('teacher/material.html', material=material, classroom=classroom, attachments=attachments)

@bp.route('/material/<int:material_id>/edit', methods=('POST',))
def edit_material(material_id):
    material, _ = _check_material(material_id)

    old_title = material.title
    old_description = material.description

    title = request.form.get('title', '')
    description = request.form.get('description', '')
    files = [f for f in request.files.getlist('files') if f.filename]
    urls = [u.rstrip(',') for u in request.form.get('links', '').split() if u.rstrip(',')]

    try:
        for url in urls:
            parts = urlparse(url)
            if parts.scheme not in ('http', 'https') or not parts.hostname: 
                raise ValueError("Invalid URL: " + url)
        if files:
            check_files(files)

        existing_attachments = material.get_attachments()
        existing_files = len([i for i in existing_attachments if isinstance(i, FileAttachment)])
        existing_links = len(existing_attachments) - existing_files
        
        if existing_links + len(urls) > app.config['MAX_LINKS']:
            raise ValueError(f"Total link attachment limit exceeded. You can attach a maximum of {app.config['MAX_LINKS']} links. You currently have {existing_links} link(s) attached to this material.")
        if existing_files + len(files) > app.config['MAX_FILES']:
            raise ValueError(f"Total file attachment limit exceeded. You can attach a maximum of {app.config['MAX_FILES']} files. You currently have {existing_files} file(s) attached to this material. Please remove some files or compress them into a single zip file if you need to upload many files.")

        material.update(title, description)

        if files:
            uploaded_files = upload_files(files)

            for filename, stored_filename, mime_type, file_size_kb in uploaded_files:
                try:
                    material.attach_file(g.user.id, stored_filename, filename, mime_type, file_size_kb)
                except Exception as e:
                    _delete_file(stored_filename)
                    material.update(old_title, old_description)
                    raise ValueError(f"Error occurred while creating file attachments: {e}")
        for url in urls:
            material.attach_link(g.user.id, url, urlparse(url).hostname or url)
        
        flash('Material updated successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('teacher.material', material_id=material.id))

@bp.route('/material/<int:material_id>/delete', methods=('POST',))
def delete_material(material_id):
    material, classroom = _check_material(material_id)
    try:
        material.delete()
        flash("Material deleted successfully.")
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('teacher.material', material_id=material.id))

    return redirect(url_for('teacher.classroom', classroom_id=classroom.id))

@bp.route('/student/<int:student_id>/', methods=('GET',))
def student(student_id):
    student = User.get_by_id(student_id)
    if not student or student.role != UserRole.STUDENT:
        abort(404)
    classrooms = [classroom for classroom in g.user.get_classrooms() if student.id in [s.id for s in classroom.get_students()]]
    if not classrooms:
        abort(404)
    assignments_completions_rows = [(assignment, ProgressRecord.get_progress(student, assignment)) for classroom in classrooms for assignment in classroom.get_assignments(True)]
    return render_template('teacher/student.html', student=student, assignments_completions_rows=assignments_completions_rows)

@bp.route('/submission/<int:submission_id>/', methods=('GET',))
def submission(submission_id):
    submission, assignment, _ = _check_submission(submission_id)
    attachments = submission.get_attachments()
    student = User.get_by_id(submission.student_id)
    return render_template('teacher/submission.html', submission=submission, assignment=assignment, attachments=attachments, student=student)

@bp.route('/submission/<int:submission_id>/give_feedback', methods=('POST',))
def give_feedback(submission_id):
    submission, _, _ = _check_submission(submission_id)
    try:
        feedback = request.form.get('feedback', '').strip()
        submission.add_feedback(feedback)
        flash('Feedback added successfully.')
    except ValueError as ve:
        flash(str(ve))

    return redirect(url_for('teacher.submission', submission_id=submission.id))


def _check_classroom(classroom_id):
    classroom = Classroom.get_by_id(classroom_id)
    if not classroom or classroom.teacher_id != g.user.id:
        abort(404)
    return classroom

def _progress_rows(assignment, classroom, teacher):
    unresolved_requests = {(help_request.student_id, help_request.assignment_id): help_request for help_request in HelpRequest.get_unresolved_for_teacher(teacher.id)}
    rows = []
    for student in classroom.get_students():
        progress = ProgressRecord.get_progress(student, assignment)
        submission = Submission.get_by_student_and_assignment(student, assignment)
        rows.append((student, progress, submission, unresolved_requests.get((student.id, assignment.id))))
    return rows

def _owns_assignment(assignment_id):
    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        abort(404)
    classroom = Classroom.get_by_id(assignment.classroom_id)
    if not classroom or classroom.teacher_id != g.user.id:
        abort(404)
    return assignment, classroom

def _check_help_request(help_request_id):
    help_request = HelpRequest.get_by_id(help_request_id)
    if not help_request:
        abort(404)
    assignment = Assignment.get_by_id(help_request.assignment_id)
    if not assignment:
        abort(404)
    classroom = Classroom.get_by_id(assignment.classroom_id)
    if not classroom or classroom.teacher_id != g.user.id:
        abort(404)
    return help_request, assignment, classroom

def _check_material(material_id):
    material = Material.get_by_id(material_id)
    if not material:
        abort(404)
    classroom = Classroom.get_by_id(material.classroom_id)
    if not classroom or classroom.teacher_id != g.user.id:
        abort(404)
    return material, classroom

def _check_submission(submission_id):
    submission = Submission.get_by_id(submission_id)
    if not submission:
        abort(404)
    assignment = Assignment.get_by_id(submission.assignment_id)
    if not assignment:
        abort(404)
    classroom = Classroom.get_by_id(assignment.classroom_id)
    if not classroom or classroom.teacher_id != g.user.id:
        abort(404)
    return submission, assignment, classroom