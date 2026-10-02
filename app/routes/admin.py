from flask import Blueprint, g, redirect, render_template, url_for
from app.security.decorators import check_role
from app.models.enums import UserRole

bp = Blueprint('admin', __name__, url_prefix='/admin')
bp.before_request(check_role(UserRole.ADMIN.value))

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('admin.dashboard'))
