from flask import render_template, Request, redirect, Response
from flask.globals import session

from queryhandler import run_query

from validators import login_validator
import bcrypt

# GET
# ---- DISPLAY PAGE WITH LOGIN FORM ----
def show():
    return render_template(
        'login.html',
        title="Log into B-Sides",
        alerts=[],
        session=session
    )

# POST
# ---- ATTEMPT TO LOG IN THE USER ----
def login(request: Request):
    validated = login_validator.validate(request)
    
    



    

# GET
# ---- DISPLAY PAGE WITH LOGIN FORM WITH ERRORS ----
def error(error):
    pass

