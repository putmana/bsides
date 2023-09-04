from flask import render_template, Request, redirect, Response
from flask.globals import session

from queryhandler import run_query

from controllers import board_controller

from validators import post_validator

import os

# GET
# ---- DISPLAY PAGE WITH ALL POSTS ON A BOARD ----
def fetch_all(board_name: str) -> str or Response:
    try:
        # Make sure the board exists
        board = board_controller.fetch_one(board_name)
        if board == None: return redirect('/pnf')

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
        """ % (board['name'])

        results = run_query(query)

        return render_template(
            'board.html', 
            name='/%s' % (board['name']), 
            posts=results, 
            title=f"/{board['name']}",
            alerts=[],
            session=session
        )

    except Exception as err:
        print(f"ERROR: {err}")
        return redirect('/pnf')
        

def fetch_one(post_id):
    pass

# GET
# ---- DISPLAY NEW POST FORM ----
def make(board_name: str) -> redirect or Response:
    # Make sure the board exists
    board = board_controller.fetch_one(board_name)
    if board == None: return redirect('/pnf')

    return render_template(
        'post.html',
        board=board['name'],
        title=f"Post to /{board['name']}",
        alerts=[],
        session=session
    )

# POST
# ---- PROCESS NEW POST FORM ----
def store(board_name: str, request: Request):
    try:
        # Make sure the board exists
        board = board_controller.fetch_one(board_name)
        assert(board, "Board does not exist")

        # Validate the request
        validated = post_validator.validate(request)

        # Store the image to the disk
        validated['file'].save(os.path.join(os.getenv("UPLOAD_FOLDER"), validated['file_name']))

        # Generate and run the database query
        query = """
            INSERT INTO
            boardposts (id, board_id, user_id, datetime, caption, imagepath)

            values (%s, %s, %s, %s, %s, %s)
        """ % (validated['id'], board['id'], session['user_id'], validated['caption'], validated['file_name'])

        run_query(query)

        # Redirect the user back to the board page
        return redirect(f"/b/{board['name']}")
    
    except Exception as err:
        print(err)
        return error(board['name'], err)

# GET
# ---- DISPLAY NEW POST FORM WITH ERROR MESSAGE ----
def error(board_name, error):
    # Make sure the board exists
    board = board_controller.fetch_one(board_name)
    if board == None: return redirect('/pnf')

    return render_template(
        'post.html',
        board=board['name'],
        title=f"Post to /{board['name']}",
        alerts=[error],
        session=session
    )