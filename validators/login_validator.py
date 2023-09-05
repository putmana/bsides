from flask import Request

import bcrypt

from controllers import user_controller
from exceptions import ValidationError

MSG_LOGIN_INVALID = "Incorrect email or password."

def validate(request: Request):

    email = request.form['email']

    # Attempt to fetch a user from the database with the provided email
    user = user_controller.fetch_credentials(email)
    if user is None: 
        raise ValidationError(MSG_LOGIN_INVALID)

    # Check that the entered password is correct
    password = request.form['password'].encode('utf8')
    password_hash = user['password'].encode('utf8') 
    if not bcrypt.checkpw(password, password_hash): 
        raise ValidationError(MSG_LOGIN_INVALID)

    return {
        'id': user['id'],
        'email': user['email'],
        'username': user['username']
    }