from flask import Flask, render_template, request, redirect, flash, session
from flask.globals import session

from authenticated import authenticated, loggedout
from controllers import post_controller, login_controller, signup_controller

from utils import env

app = Flask(__name__)
app.secret_key = env("APP_SECRET_KEY")


##################
# ERROR HANDLING #
##################
@app.errorhandler(401)
def error401(e) -> str:
    return render_template(
        'error.html', 
        title="401", 
        code="401",
        text="Nope.",
        alerts=[], 
        session=session
    )

@app.errorhandler(403)
def error403(e) -> str:
    return render_template(
        'error.html', 
        title="403", 
        code="403",
        text="Definitely not.",
        alerts=[], 
        session=session
    )

@app.errorhandler(404)
def error404(e) -> str:
    return render_template(
        'error.html', 
        title="404", 
        code="404",
        text="Can't find it.",
        alerts=[], 
        session=session
    )

@app.errorhandler(Exception) # Internal server errors
def error500(e) -> str:
    alerts = []
    if env("APP_DEBUG"): alerts = [e]

    return render_template(
        'error.html',
        title="500",
        code="500",
        text="Whoops.",
        alerts=alerts,
        session=session
    )




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
    return post_controller.fetch_by_board(board_name)



#################
# NEW POST PAGE #
################
@app.route('/b/<string:board_name>/post', methods=['GET'])
@authenticated
def b_board_make(board_name):
    return post_controller.make(board_name)

@app.route('/b/<string:board_name>/post', methods=['POST'])
@authenticated
def b_board_store(board_name) -> str:
    return post_controller.store(board_name, request)



#############
# USER PAGE #
#############
@app.route('/u/<string:username>', methods=['GET'])
def u_user_get(username):
    return post_controller.fetch_by_user(username)



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



###############################
### +++ RUN APPLICATION +++ ###
###############################
if __name__ == "__main__":
    app.run(
        debug=env("APP_DEBUG"),
        port=env("APP_PORT")
    )