from queryhandler import run_query

def fetch_by_name(user_name):
    query = """
        SELECT
        u.id,
        u.username

        FROM
        users as u

        WHERE
        u.username = %s
    """

    results = run_query(query, [user_name])

    # Return None if the user does not exist
    if len(results) == 0:
        return False
    
    return {
        'id': results[0][0],
        'username': results[0][1]
    }



def fetch_credentials(email):
    # Fetch the user by email
    query = """
        SELECT
        u.id, u.username, u.email, u.password

        FROM
        users as u

        WHERE
        email = %s
    """

    results = run_query(query, [email])

    if (len(results) == 0): return None

    return {
        'id': results[0][0],
        'username': results[0][1],
        'email': results[0][2],
        'password': results[0][3]
    }
    
def email_is_unique(email):
    # Check for a user that uses the email provided
    query = """
        SELECT
        u.id

        FROM
        users as u

        WHERE
        email = %s
    """

    results = run_query(query, [email])

    if len(results) == 0: return True
    return False

def username_is_unique(username):
    # Check for a user that uses the username provided
    query = """
        SELECT
        u.id

        FROM
        users as u

        WHERE
        email = %s
    """

    results = run_query(query, [username])

    if len(results) == 0: return True
    return False




