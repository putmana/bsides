from sshtunnel import SSHTunnelForwarder
import sql_config
from DBcm import UseDatabase

import uuid

import time

import queryhandler

DATABASE = "bsides"
SERVER = "159.223.106.213"


# GET QUERIES
def getPosts(boardname):
    query = """
        SELECT
        u.displayname, bp.datetime, bp.caption, bp.id, bp.imagepath

        FROM boardposts AS bp

        JOIN users AS u
        ON bp.user_id = u.id

        JOIN boards AS b
        ON bp.board_id = b.id

        WHERE
        b.name = '%s'

        ORDER BY
        bp.datetime
        DESC           
    """ % (boardname)

    return query.run_query(query)

def getUserPosts(username):
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = """
            SELECT
            b.name, bp.datetime, bp.caption, bp.id, bp.imagepath

            FROM boardposts AS bp

            JOIN users AS u
            ON bp.user_id = u.id

            JOIN boards AS b
            ON bp.board_id = b.id

            WHERE
            u.username = '%s'

            ORDER BY
            bp.datetime
            DESC           
        """ % (username)

        cursor.execute(query)
        result = cursor.fetchall()

    return result
    
def getAllBoards():
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = """
            SELECT
            b.name

            FROM boards as b

            ORDER BY
            b.id

        """

        cursor.execute(query)
        result = cursor.fetchall()

    return result
    
def getBoardID(boardname):
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = """
            SELECT
            b.id

            FROM 
            boards as b

            WHERE
            b.name = '%s'
        """ % boardname

        cursor.execute(query)
        result = cursor.fetchall()
    
    if len(result) == 0: return False

    return result[0][0]

def getUserID(username):
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = """
            SELECT
            u.id

            FROM 
            users as u

            WHERE
            u.username = '%s'
        """ % username

        cursor.execute(query)
        result = cursor.fetchall()
    
    if len(result) == 0: return False

    return result[0][0]

def userLogin(email, password):
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = f"""
            SELECT
            u.id, u.username, u.email

            FROM 
            users as u

            WHERE
            u.email = '{email}'
            AND
            u.password = '{password}'
        """

        cursor.execute(query)
        result = cursor.fetchall()

    if len(result) == 0: return 'FAIL'

    return result

# POST QUERIES
def makePost(postid, boardid, userid, datetime, caption, imagepath):
    with UseDatabase(sql_config.dbconfig) as cursor:
        query = """use %s""" % (DATABASE)
        cursor.execute(query)

        query = """
            INSERT INTO 
            boardposts (id, board_id, user_id, datetime, caption, imagepath)

            VALUES (%s, %s, %s, %s, %s, %s)

        """

        cursor.execute(query, (postid, boardid, userid, datetime, caption, imagepath))

def makeNewAccount(email, username, password):
    u_UUID = str(uuid.uuid4())
    u_email = email
    u_username = username
    u_password = password
    u_displayname = username

    with SSHTunnelForwarder((SERVER, 22), **sql_config.sshconfig) as tunnel:
        with UseDatabase(sql_config.dbconfig) as cursor:

            exitcode = 'NONE'
            
            

            query = """use %s""" % (DATABASE)
            cursor.execute(query)
            query = f"""
                SELECT
                u.username
                FROM
                users as u

                WHERE
                u.username = '{u_username}'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) > 0:
                exitcode = 'FAIL_USN'
                return exitcode

            query = f"""
                SELECT
                u.email
                FROM
                users as u

                WHERE
                u.email = '{u_email}'
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if len(results) > 0:
                exitcode = 'FAIL_EML'
                return exitcode

            if exitcode == 'NONE':
                query = """
                    INSERT INTO 
                    users (id, email, username, password, displayname)

                    VALUES (%s, %s, %s, %s, %s)

                """
                cursor.execute(query, (u_UUID, u_email, u_username, u_password, u_displayname))
                exitcode = 'SUCCESS'

        return exitcode