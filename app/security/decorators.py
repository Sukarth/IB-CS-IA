from flask import g, redirect, url_for, abort, flash
from functools import wraps


def check_login():
    """Is a guard to check if user is logged in. A response means the user is not logged in, None means they are logged in."""
    if g.user is None:
        flash('You must be logged in to access this page.')
        return redirect(url_for('auth.login'))
    return None

def check_role(role):
    """Builds a guard to check if a user has a given role. A response means invalid/blocked, None means the role is valid."""
    def guard():
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user.role != role:
            abort(403)
        return None
    return guard


def _as_decorator(guard):
    """Turns a guard into a decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            blocked = guard()
            if blocked is not None:
                return blocked
            return func(*args, **kwargs)
        return wrapper
    return decorator


login_required = _as_decorator(check_login) # better decorator naming

def role_required(role): # better decorator naming
    return _as_decorator(check_role(role))