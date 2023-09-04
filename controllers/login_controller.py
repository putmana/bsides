from flask import render_template, Request, redirect
from flask.globals import session

from validators import login_validator

# GET
# ---- DISPLAY PAGE WITH LOGIN FORM ----
def show(alerts: []):
    return render_template(
        'login.html',
        title="Log into B-Sides",
        alerts=alerts,
        session=session
    )

# POST
# ---- ATTEMPT TO LOG IN THE USER ----
def login(request: Request):
    try:
        # Validate the request
        validated = login_validator.validate(request)

        # Set the session to the user
        session["user_id"] = validated["id"]
        session["username"] = validated["username"]
        session["email"] = validated["email"]

        return redirect("/b")
    
    except AssertionError as err:
        return show([err])
    
# GET
# ---- LOG OUT THE USER ----
def logout():
    session.pop('user_id')
    session.pop('username')
    session.pop('email')

    return redirect('/login')