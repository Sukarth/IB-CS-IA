from flask import Blueprint, g, redirect, url_for
from app.models.enums import UserRole

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    elif g.user.role == UserRole.ADMIN.value:
        return redirect(url_for('admin.dashboard'))
    elif g.user.role == UserRole.TEACHER.value:
        return redirect(url_for('teacher.dashboard'))
    elif g.user.role == UserRole.STUDENT.value:
        return redirect(url_for('student.dashboard'))
    else:
        return redirect(url_for('auth.login'))