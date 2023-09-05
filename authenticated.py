from flask import session, redirect
from functools import wraps


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper


def loggedout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return redirect("/logout")
        return func(*args, **kwargs)
    return wrapper
