from flask import Flask, render_template, request, redirect, flash, session
from flask.globals import session

from authenticated import authenticated, loggedout
from controllers import post_controller, login_controller, signup_controller


app = Flask(__name__)
app.secret_key = "B-SIDES-KEY"

###############
# ERROR PAGES #
###############
@app.errorhandler(404)
def error404(e) -> str:
    return redirect('/pnf')

@app.route('/pnf', methods=['GET'])
def pnf() -> str:
    return render_template('pagenotfound.html', title="404", alerts=[], session=session)



#############
# HOME PAGE #
#############
@app.route('/', methods=['GET'])
def home() -> str:
    return redirect('/b')

@app.route('/b', methods=['GET'])
def b_get() -> str:
    return render_template('boardlist.html', title="Boards", alerts=[], session=session)



##############
# BOARD PAGE #
##############
@app.route('/b/<string:board_name>', methods=['GET'])
def b_board_show(board_name):
    return post_controller.fetch_all(board_name)



#################
# NEW POST PAGE #
################
@app.route('/b/<string:board_name>/post', methods=['GET'])
@authenticated
def b_board_make(board_name):
    return post_controller.make(board_name)

@app.route('/b/<string:boardname>/post', methods=['POST'])
@authenticated
def b_board_store(board_name) -> str:
    return post_controller.store(board_name, request)



#############
# USER PAGE #
#############
@app.route('/u/<string:username>', methods=['GET'])
def u_user_get():
    return redirect('/b') # Not quite ready yet



#######################
# LOGIN & LOGOUT PAGE #
#######################
@app.route('/login', methods=['GET'])
@loggedout
def login_get():
    return login_controller.show()

@app.route('/login', methods=['POST'])
@loggedout
def login_login():
    return login_controller.login(request)

@app.route('/logout', methods=['GET'])
@authenticated
def logout():
    return login_controller.logout()



###############
# SIGNUP PAGE #
###############
@app.route('/signup', methods=['GET'])
@loggedout
def signup_get():
    return signup_controller.show()

@app.route('/signup', methods=['POST'])
@loggedout
def signup_signup():
    return signup_controller.signup(request)

app.run(debug=True)