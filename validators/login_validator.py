from flask import Request

def validate(request: Request):
    # Validate the email address
    email = request.form['email']
    assert(email != "", "Email cannot be blank")

    # Validate the password
    password = request.form['password']
    assert(password != "", "Password cannot be blank")

    return {
        'email': email,
        'password': password
    }


    
