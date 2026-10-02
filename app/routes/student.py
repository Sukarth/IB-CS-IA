from flask import Blueprint, g, redirect, render_template, url_for
from app.security.decorators import check_role
from app.models.enums import UserRole
from app.models.assignment import Assignment
from app.models.user import User

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