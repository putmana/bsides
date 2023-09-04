from flask import Request

import bcrypt

from controllers import user_controller

INVALID_LOGIN_MSG = "Incorrect email or password."

def validate(request: Request):

    email = request.form['email']
    password = request.form['password']

    # Attempt to fetch a user from the database with the provided email
    user = user_controller.fetch_credentials(email)

    # Check that a user with the entered email address exists
    assert user != None, INVALID_LOGIN_MSG

    # Check that the entered password matches the returned user

    print(user['password'])
    assert bcrypt.checkpw(password.encode('utf8'), user['password'].encode('utf8')), INVALID_LOGIN_MSG

    return {
        'id': user['id'],
        'email': user['email'],
        'username': user['username']
    }