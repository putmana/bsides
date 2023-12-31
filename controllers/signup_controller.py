from flask import render_template, Request, redirect
from flask.globals import session

from queryhandler import run_query
from validators import signup_validator
from exceptions import ValidationError


# GET
# ---- DISPLAY PAGE WITH REGISTER FORM ----
def show(alerts=[]):
    return render_template(
        "signup.html",
        title="Sign up to B-Sides",
        alerts=alerts,
        session=session
    )


# POST
# ---- ATTEMPT TO SIGN UP THE USER ----
def signup(request: Request):
    try:
        # Validate the request
        validated = signup_validator.validate(request)

        # Generate and run the database query
        query = """
            INSERT INTO
            users (id, email, username, password)

            VALUES (%s, %s, %s, %s)
        """

        run_query(query, [validated["id"], validated["email"],
                  validated["username"], validated["password"]])

        return redirect("/login")

    except ValidationError as err:
        return show([err])
