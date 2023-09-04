from queryhandler import run_query

def fetch_credentials(email):
    # Fetch the user by email
    query = """
        SELECT
        u.id, u.username, u.email, u.password

        FROM
        users as u

        WHERE
        email = '%s'
    """ % email

    results = run_query(query)

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
        email = '%s'
    """ % (email)

    results = run_query(query)

    if len(results != 0): return False

def username_is_unique(username):
    # Check for a user that uses the username provided
    query = """
        SELECT
        u.id

        FROM
        users as u

        WHERE
        email = '%s'
    """ % (username)

    results = run_query(query)

    if len(results != 0): return False





