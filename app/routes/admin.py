from flask import Blueprint, g, redirect, render_template, url_for, request, flash, abort, current_app as app, session
from app.security.decorators import check_role
from app.models.enums import UserRole
from app.models.user import User
from app.models.year_group import YearGroup
from app.models.activation_key import ActivationKey

bp = Blueprint('admin', __name__, url_prefix='/admin')
bp.before_request(check_role(UserRole.ADMIN.value))

@bp.route('/dashboard')
def dashboard():
    try:
        role = request.args.get('role', None, type=UserRole)
        year_group = request.args.get('year_group', None, type=int)
        activated = {'activated': True, 'not_activated': False}.get(request.args.get('activated'))
        
        if year_group and role != UserRole.STUDENT:
            if role:
                flash("The filter role has automatically been set to 'Student', as filtering by year group is only applicable to students.")
        role = UserRole.STUDENT
        
        users = User.get_all(role, year_group, activated)

        year_groups = YearGroup.get_all()
        key_count = ActivationKey.get_count()
        year_group_names = {group.id: group.name for group in year_groups}

    except ValueError as ve:
        flash(str(ve))
        return render_template('admin/dashboard.html', users=[], year_groups=[], key_count=0, role=None, year_group=None, activated=None, year_group_names={})

    return render_template('admin/dashboard.html', users=users, year_groups=year_groups, key_count=key_count, role=role, year_group=year_group, activated=activated, year_group_names=year_group_names)

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('admin.dashboard'))

@bp.route('/year_group/<int:year_group_id>')
def year_group(year_group_id):
    try:
        year_group = _check_year_group(year_group_id)
        students = year_group.get_students()
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/year_group.html', year_group=year_group, students=students)

@bp.route('/year_group/create', methods=('POST',))
def create_year_group():
    name = request.form.get('name', '').strip()
    try:
        year_group = YearGroup.create(name)
        flash(f'Year group "{year_group.name}" created successfully.')
    except ValueError as ve:
        flash(str(ve))
    return redirect(url_for('admin.dashboard'))

@bp.route('/year_group/<int:year_group_id>/rename', methods=('POST',))
def rename_year_group(year_group_id):
    new_name = request.form.get('name', '').strip()    
    try:
        year_group = _check_year_group(year_group_id)
        year_group.rename(new_name)
        flash(f'Year group renamed successfully to "{year_group.name}".')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.year_group', year_group_id=year_group.id))

@bp.route('/year_group/<int:year_group_id>/delete', methods=('POST',))
def delete_year_group(year_group_id):
    try:
        year_group = _check_year_group(year_group_id)
        year_group.delete()
        flash(f'Year group "{year_group.name}" deleted successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.dashboard'))

@bp.route('/year_group/<int:year_group_id>/add_student', methods=('POST',))
def add_student_to_year_group(year_group_id):
    year_group = _check_year_group(year_group_id)
    student_id = request.form.get('add_student_id', 0, type=int)
    student = User.get_by_id(student_id)
    
    if not student or student.role != UserRole.STUDENT:
        flash("No student found for the provided ID.")
        return redirect(url_for('admin.year_group', year_group_id=year_group.id))
    try:
        year_group.add_student(student)
        flash(f'Student "{student.name}" added successfully to year group "{year_group.name}".')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.year_group', year_group_id=year_group.id))

@bp.route('/year_group/<int:year_group_id>/remove_student', methods=('POST',))
def remove_student_from_year_group(year_group_id):
    year_group = _check_year_group(year_group_id)
    student_id = request.form.get('remove_student_id', 0, type=int)
    student = User.get_by_id(student_id)
    
    if not student or student.role != UserRole.STUDENT:
        flash("No student found for the provided ID.")
        return redirect(url_for('admin.year_group', year_group_id=year_group.id))
    try:
        year_group.remove_student(student)
        flash(f'Student "{student.name}" removed successfully from year group "{year_group.name}".')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.year_group', year_group_id=year_group.id))

@bp.route('/activation_keys')
def activation_keys():
    key_count = ActivationKey.get_count()
    return render_template('admin/activation_keys.html', key_count=key_count, new_keys=session.pop('new_keys', []), max_count=app.config['MAX_KEYS_PER_GENERATION'], year_groups=YearGroup.get_all(), keys=ActivationKey.get_all())

@bp.route('/activation_keys/generate', methods=('POST',))
def generate_activation_keys():
    role = request.form.get('role', None, type=UserRole)
    valid_days = request.form.get('validity', 1, type=int)
    count = request.form.get('count', 1, type=int)
    year_group_id = request.form.get('year_group_id', 0, type=int)
    
    try:
        if not role:
            raise ValueError("Role must be specified.")

        if role == UserRole.STUDENT and not year_group_id:
            raise ValueError("Year group ID must be specified for creating student activation keys.")

        if not 1 <= count <= app.config['MAX_KEYS_PER_GENERATION']:
            raise ValueError(f"You can only generate 1-{app.config['MAX_KEYS_PER_GENERATION']} activation keys at once.")

        if role == UserRole.STUDENT:
            year_group = YearGroup.get_by_id(year_group_id)
            if not year_group:
                raise ValueError("No year group found for the provided ID.")
            
            keys = ActivationKey.generate_batch(role, g.user, valid_days, count, year_group.id)
        else:
            keys = ActivationKey.generate_batch(role, g.user, valid_days, count)

        session['new_keys'] = keys
        flash(f'Successfully generated {len(keys)} activation key(s). Please save them now as they will not be shown again.')
    
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.activation_keys'))


@bp.route('/activation_keys/<int:key_id>/delete', methods=('POST',))
def delete_activation_key(key_id):
    key = ActivationKey.get_by_id(key_id)
    
    if not key:
        flash("No activation key found for the provided ID.")
        return redirect(url_for('admin.activation_keys'))
    
    try:
        key.delete()
        flash(f'Activation key deleted successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.activation_keys'))


@bp.route('/user/<int:user_id>/deactivate', methods=('POST',))
def deactivate_user(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        flash("No user found for the provided ID.")
        return redirect(url_for('admin.dashboard'))
    
    if user.id == g.user.id:
        flash("You cannot deactivate your own account.")
        return redirect(url_for('admin.dashboard'))

    try:
        user.deactivate()
        flash(f'User "{user.name}" deactivated successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.dashboard'))

@bp.route('/user/<int:user_id>/activate', methods=('POST',))
def activate_user(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        flash("No user found for the provided ID.")
        return redirect(url_for('admin.dashboard'))
    
    try:
        user.activate()
        flash(f'User "{user.name}" activated successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.dashboard'))

@bp.route('/user/<int:user_id>/change_year_group', methods=('POST',))
def change_year_group(user_id):
    user = User.get_by_id(user_id)
    
    if not user or user.role != UserRole.STUDENT:
        flash("No student found for the provided ID.")
        return redirect(url_for('admin.dashboard'))

    new_year_group = YearGroup.get_by_id(request.form.get('year_group_id', 0, type=int))
    
    if not new_year_group:
        flash("No year group found for the provided ID.")
        return redirect(url_for('admin.dashboard'))
    
    try:
        if user.year_group_id:
            YearGroup.get_by_id(user.year_group_id).remove_student(user)
                   
        YearGroup.get_by_id(new_year_group.id).add_student(user)
        flash(f'User "{user.name}" moved to year group "{new_year_group.name}" successfully.')
    except ValueError as ve:
        flash(str(ve))
    
    return redirect(url_for('admin.dashboard'))

def _check_year_group(year_group_id: int):
    year_group = YearGroup.get_by_id(year_group_id)
    if not year_group:
        abort(404)
    return year_group