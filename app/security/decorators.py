from flask import g, redirect, url_for
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
                return redirect(url_for('auth.login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator