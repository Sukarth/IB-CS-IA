from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from app.security.decorators import check_login
from app.models.user import User
import secrets

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        activation_key = request.form['activation_key'].upper()

        try:
            User.register(name, email, password, activation_key)
            flash('User registered successfully.')
            return redirect(url_for('auth.login'))
        except ValueError as ve:
            flash(str(ve))
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.authenticate(email, password)
            if user:
                session.clear()
                session['user_id'] = user.id
                flash('Logged in successfully.')
                return redirect(url_for('main.index'))
        except ValueError as ve:
            flash(str(ve))
    return render_template('auth/login.html')

@bp.route('/logout', methods=('POST',))
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@bp.route('/account', methods=('GET',))
def account():
    logged_in = check_login()
    if logged_in:
        return logged_in
    return render_template('auth/account.html')

@bp.route('/account/profile', methods=('POST',))
def update_profile():
    logged_in = check_login()
    if logged_in:
        return logged_in
    try:
        g.user.update_profile(request.form.get('name', ''), request.form.get('email', ''))
        flash('Profile updated successfully.')
    except ValueError as ve:
        flash(str(ve))
    return redirect(url_for('auth.account'))

@bp.route('/account/password', methods=('POST',))
def change_password():
    logged_in = check_login()
    if logged_in:
        return logged_in
    try:
        g.user.change_password(request.form.get('current_password', ''), request.form.get('new_password', ''))
        flash('Password changed successfully.')
    except ValueError as ve:
        flash(str(ve))
    return redirect(url_for('auth.account'))

@bp.before_app_request
def load_logged_in_user():
    g.user = None
    user_id = session.get('user_id')
    if user_id is None:
        return
    
    user = User.get_by_id(user_id)
    if user is None or not user.is_active:
            session.clear()
            flash('Your session has ended. Please log in again.')
            return
    g.user = user

@bp.before_app_request
def csrf_protection():
    if request.method == 'POST':
        token = session.get('_csrf_token')
        form_token = request.form.get('_csrf_token')
        if not token or token != form_token:
            abort(400)

@bp.app_context_processor
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_urlsafe(32)
    return {'csrf_token': session['_csrf_token']}
        