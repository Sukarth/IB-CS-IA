from flask import g, redirect, url_for, abort, flash
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if g.user is None or g.user.role != role:
                flash('Access denied.')
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator