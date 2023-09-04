from flask import Flask, render_template, request, redirect, flash, session
from flask.globals import session
import query__old

from authenticated import authenticated, loggedout

from controllers import post_controller

# from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "B-SIDES-KEY"

@app.errorhandler(404)
def error404(e) -> str:
    return redirect('/pnf')

@app.route('/pnf', methods=['GET'])
def pnf() -> str:
    return render_template('pagenotfound.html', title="404", alerts=[], session=session)

@app.route('/', methods=['GET'])
def home() -> str:
    return redirect('/b')

@app.route('/b', methods=['GET'])
def b_get() -> str:
    return render_template('boardlist.html', title="Boards", alerts=[], session=session)

@app.route('/b/<string:board_name>', methods=['GET'])
def b_board_get(board_name):
    return post_controller.fetch_all(board_name)

@app.route('/b/<string:board_name>/post', methods=['GET'])
@authenticated
def b_board_make(board_name):
    return post_controller.make(board_name)

@app.route('/b/<string:boardname>/post', methods=['POST'])
@authenticated
def b_board_store(board_name) -> str:
    return post_controller.store(board_name, request)


@app.route('/u/<string:username>', methods=['GET'])
def userpage(username) -> str:
    if vp.user(username):
        posts = query__old.getUserPosts(username)
        return render_template('profile.html', name=username, posts=posts, title=f"@{username}", alerts=[], session=session)
    else:
        return redirect('/pnf')

@app.route('/login', methods=['GET'])
@loggedout
def loginpage() -> str:
    return render_template('login.html', title="Log into B-Sides", alerts=[], session=session)

@app.route('/login', methods=['POST'])
@loggedout
def process_login():
    email = request.form['email']
    password = request.form['password']
    userInfo = query__old.userLogin(email, password)
    if userInfo == 'FAIL':
        return redirect('/login$FAIL')
    else:
        session['user_id'] = userInfo[0][0]
        session['username'] = userInfo[0][1]
        session['email'] = userInfo[0][2]
        return redirect('/b')

@app.route('/login$FAIL', methods=['GET'])
@loggedout
def loginpagefail() -> str:
    return render_template('login.html', title="Log into B-Sides", alerts=['Incorrect email or password!'], session=session)

@app.route('/login$LOGOUT', methods=['GET'])
@loggedout
def loginpagelogout() -> str:
    return render_template('login.html', title="Log into B-Sides", alerts=['Logged out of current session!'], session=session)

@app.route('/login$NEWACC', methods=['GET'])
@loggedout
def loginpagenewaccount() -> str:
    return render_template('login.html', title="Log into B-Sides", alerts=['Account created successfully! You can now log in.'], session=session)

@app.route('/logout', methods=['GET'])
@authenticated
def logout() -> str:
    session.pop('user_id')
    session.pop('username')
    session.pop('email')

    return redirect('/login$LOGOUT')

@app.route('/signup', methods=['GET'])
@loggedout
def signuppage() -> str:
    return render_template('signup.html', title="Sign up to B-Sides", alerts=[], session=session)

@app.route('/signup$FAIL_PWD', methods=['GET'])
@loggedout
def signuppage_failpwd() -> str:
    return render_template('signup.html', title="Sign up to B-Sides", alerts=['Passwords do not match!'], session=session)

@app.route('/signup$FAIL_USN', methods=['GET'])
@loggedout
def signuppage_failusn() -> str:
    return render_template('signup.html', title="Sign up to B-Sides", alerts=['Username is already in use!'], session=session)

@app.route('/signup$FAIL_EML', methods=['GET'])
@loggedout
def signuppage_faileml() -> str:
    return render_template('signup.html', title="Sign up to B-Sides", alerts=['Email is already in use!'], session=session)

@app.route('/signup$FAIL_UNK', methods=['GET'])
@loggedout
def signuppage_failunk() -> str:
    return render_template('signup.html', title="Sign up to B-Sides", alerts=['An unknown error occured.'], session=session)


@app.route('/signup', methods=['POST'])
@loggedout
def process_signup():
    print("We got here")
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    verified = request.form['verified']

    if password == verified:
        accstat = query__old.makeNewAccount(email, username, password)

        if accstat == 'FAIL_EML':
            return redirect('/signup$FAIL_EML')
        elif accstat == 'FAIL_USN':
            return redirect('/signup$FAIL_USN')
        elif accstat == 'SUCCESS':
            return redirect('/login$NEWACC')
        else:
            return redirect('/signup$FAIL_UNK')
    else:
        return redirect('/signup$FAIL_PWD')

app.run(debug=True)