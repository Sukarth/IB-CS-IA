from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        activation_key = request.form['activation_key']

        try:
            User.register(name, email, password, activation_key)
        except Exception as e:
            flash(str(e))
        return redirect(url_for('auth.login'))
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
                return redirect(url_for('index'))
        except Exception as e:
            flash(str(e))

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.get_by_id(user_id)
