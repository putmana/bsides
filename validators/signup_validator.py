from flask import Request
from controllers import user_controller

import re
import uuid
import bcrypt

from exceptions import ValidationError

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{2,}$"

USERNAME_MIN_LENGTH = 2
USERNAME_MAX_LENGTH = 20

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 200

MSG_EMAIL_INVALID = "The provided email address is invalid"
MSG_EMAIL_IN_USE = "Email address is already in use"

MSG_USERNAME_NOT_ALPHANUM = "Usernames may only contain letters, numbers, and underscores"
MSG_USERNAME_TOO_SHORT = f"Username must be at least {USERNAME_MIN_LENGTH} characters long"
MSG_USERNAME_TOO_LONG = f"Maximum username length is {USERNAME_MAX_LENGTH} characters"
MSG_USERNAME_ONLY_UNDERSCORES = "Username cannot only contain underscores"
MSG_USERNAME_IN_USE = "Username is already in use"

MSG_PASSWORDS_DONT_MATCH = "Passwords do not match"
MSG_PASSWORD_TOO_SHORT = f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
MSG_PASSWORD_TOO_LONG = f"Maximum password length is {PASSWORD_MAX_LENGTH} characters"
MSG_PASSWORD_TOO_WEAK = "Password must contain at least one letter and one number"

def validate(request: Request):
    # Generate an ID for the user
    user_id = str(uuid.uuid4())



    ############################
    # EMAIL ADDRESS VALIDATION #
    ############################
    email = request.form['email'].lower()

    # Check that the email address is valid
    if re.match(EMAIL_REGEX, email) is None:
        raise ValidationError(MSG_EMAIL_INVALID)

    # Check that the email is not already in use
    if not user_controller.email_is_unique(email):
        raise ValidationError(MSG_EMAIL_IN_USE)



    #######################
    # USERNAME VALIDATION #
    #######################
    username = request.form['username']

    # Check that the username only contains alphanumeric characters and underscores
    if not username.replace("_", "").isalnum:
        raise ValidationError(MSG_USERNAME_NOT_ALPHANUM)

    # Check that the username is not too short
    if len(username) < USERNAME_MIN_LENGTH:
        raise ValidationError(MSG_USERNAME_TOO_SHORT)
    
    # Check that the username is not too long
    if len(username) > USERNAME_MAX_LENGTH:
        raise ValidationError(MSG_USERNAME_TOO_LONG)

    # Check that the username does not only contain underscores
    if len(username.replace("_", "")) == 0:
        raise ValidationError(MSG_USERNAME_ONLY_UNDERSCORES)
    
    # Check that the username is not already in use
    if not user_controller.username_is_unique(username):
        raise ValidationError(MSG_USERNAME_IN_USE)



    #######################
    # PASSWORD VALIDATION #
    #######################
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Check that the password and confirm password fields match
    if not password == confirm_password:
        raise ValidationError(MSG_PASSWORDS_DONT_MATCH)

    # Check that the password is not too short
    if password < PASSWORD_MIN_LENGTH:
        raise ValidationError(MSG_PASSWORD_TOO_SHORT)

    # Check that the password is not too long
    if password > PASSWORD_MAX_LENGTH:
        raise ValidationError(MSG_PASSWORD_TOO_LONG)
    
    # Check that password meets complexity criteria
    if re.fullmatch(PASSWORD_REGEX, password) is None:
        raise ValidationError(MSG_PASSWORD_TOO_WEAK)

    # Encrypt the password
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

    return {
        "id": user_id,
        "email": email,
        "username": username,
        "password": hashed_password
    }



    






