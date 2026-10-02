from flask import Blueprint, g, redirect, render_template, url_for
from app.security.decorators import check_role
from app.models.enums import UserRole

bp = Blueprint('teacher', __name__, url_prefix='/teacher')
bp.before_request(check_role(UserRole.TEACHER.value))

@bp.route('/dashboard')
def dashboard():
    return render_template('teacher/dashboard.html')

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('teacher.dashboard'))